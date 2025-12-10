from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import connection, DatabaseError
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
import logging
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from apps.core.models import UserProfile, UnidadProductiva, AuditLog, PasswordResetToken
from apps.core.serializers import (
    UserProfileSerializer, UnidadProductivaSerializer, AuditLogSerializer,
    RegisterSerializer, RequestPasswordResetSerializer, PasswordResetConfirmSerializer
)
from apps.core.permissions import IsOwner, IsAdminUser, IsAdminOrOwner

logger = logging.getLogger('apps')


@api_view(["GET"])
@permission_classes([AllowAny])  # 🔓 Permite acceso anónimo para monitoreo
def health(request):
    """
    Health check endpoint - verifica la salud del servidor y base de datos.
    Usado para monitoreo externo y CI/CD.
    """
    health_data = {
        "status": "healthy",
        "timestamp": timezone.now().isoformat(),
        "server": "OK",
        "database": "OK",
    }

    try:
        # Verificar conexión a la base de datos
        connection.ensure_connection()
    except DatabaseError as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_data["database"] = "ERROR"
        health_data["status"] = "unhealthy"
        return Response(health_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        logger.error(f"Unexpected error during health check: {str(e)}")
        health_data["server"] = "ERROR"
        health_data["status"] = "unhealthy"
        return Response(health_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(health_data, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar perfiles de usuario.
    
    Filtros disponibles:
    - role: Filtrar por rol
    - is_verified: Filtrar por verificación
    - search: Búsqueda por nombre o email
    """
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_verified']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    ordering_fields = ['created_at', 'updated_at', 'user__username']
    ordering = ['-updated_at']

    def get_permissions(self):
        """Permisos por acción"""
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self):
        """Obtener objeto de perfil del usuario actual o especificado"""
        obj = super().get_object()
        if not (self.request.user.is_staff or obj.user == self.request.user):
            self.permission_denied(self.request)
        return obj

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener el perfil del usuario logueado"""
        try:
            profile = request.user.profile
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'detail': 'El usuario no tiene perfil asociado'},
                status=status.HTTP_404_NOT_FOUND
            )


class UnidadProductivaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar unidades productivas.
    
    Filtros disponibles:
    - owner: Filtrar por propietario
    - is_active: Filtrar por estado activo
    - search: Búsqueda por nombre o ubicación
    """
    queryset = UnidadProductiva.objects.select_related('owner').all()
    serializer_class = UnidadProductivaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['owner', 'is_active']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['created_at', 'updated_at', 'name', 'area_hectareas']
    ordering = ['-updated_at']

    def get_queryset(self):
        """Filtrar unidades por usuario (solo ver propias o si es staff)"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Asignar el propietario al usuario actual"""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def cultivos(self, request, pk=None):
        """Obtener cultivos de esta unidad productiva"""
        unidad = self.get_object()
        # Este endpoint sirve como base para integración con app cultivos
        return Response({
            'detail': 'Integración con app cultivos',
            'unidad_id': unidad.id,
            'unidad_name': unidad.name,
        })


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet solo lectura para registros de auditoría.
    Solo administradores pueden ver.
    
    Filtros disponibles:
    - action: Filtrar por tipo de acción
    - model_name: Filtrar por modelo
    - user: Filtrar por usuario
    """
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'model_name', 'user']
    search_fields = ['model_name', 'object_id', 'user__username']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class RegisterAPIView(APIView):
    """
    API endpoint para registro de nuevo usuario.
    
    Soporta múltiples formatos:
    - JSON: Content-Type: application/json
    - Form-data: Content-Type: application/x-www-form-urlencoded
    - Multipart-form: Content-Type: multipart/form-data
    
    POST /api/auth/register/
    {
        "username": "juan",
        "email": "juan@example.com",
        "password": "SecurePass123!",
        "password2": "SecurePass123!",
        "first_name": "Juan",
        "last_name": "Pérez"
    }
    """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description='Crear nuevo usuario con registro',
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(
                description='Usuario registrado exitosamente',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(description='Datos inválidos')
        }
    )
    def post(self, request, *args, **kwargs):
        """Crear nuevo usuario"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"Nuevo usuario registrado: {user.username}")
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description='Obtener información sobre el endpoint de registro',
        responses={
            200: openapi.Response(
                description='Información del endpoint',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'endpoint': openapi.Schema(type=openapi.TYPE_STRING),
                        'method': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'required_fields': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'example': openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """Retornar información sobre el endpoint"""
        return Response({
            'endpoint': '/api/auth/register/',
            'method': 'POST',
            'description': 'Registrar nuevo usuario',
            'required_fields': [
                'username (string, único)',
                'email (string, válido y único)',
                'password (string, mínimo 8 caracteres)',
                'password2 (string, debe coincidir con password)',
                'first_name (string)',
                'last_name (string)'
            ],
            'example': {
                'username': 'juan',
                'email': 'juan@example.com',
                'password': 'SecurePass123!',
                'password2': 'SecurePass123!',
                'first_name': 'Juan',
                'last_name': 'Pérez'
            }
        })


class RequestPasswordResetAPIView(APIView):
    """
    API endpoint para solicitar recuperación de contraseña.
    
    Soporta múltiples formatos:
    - JSON: Content-Type: application/json
    - Form-data: Content-Type: application/x-www-form-urlencoded
    
    POST /api/auth/password-reset/
    {
        "email": "usuario@example.com"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """Solicitar recuperación de contraseña"""
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Crear token de recuperación
            reset_token = PasswordResetToken.create_token(user)
            
            # Preparar URL para recuperación
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_token.token}" if hasattr(settings, 'FRONTEND_URL') else f"http://localhost:3000/reset-password/{reset_token.token}"
            
            # Enviar email
            try:
                send_mail(
                    subject='Recuperación de contraseña - AgroManager',
                    message=f"""
Hola {user.first_name},

Has solicitado recuperar tu contraseña. Haz clic en el siguiente enlace para establecer una nueva contraseña:

{reset_url}

Este enlace expira en 24 horas.

Si no solicitaste esto, ignora este correo.

Saludos,
Equipo AgroManager
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                logger.info(f"Email de recuperación enviado a: {user.email}")
            except Exception as e:
                logger.error(f"Error enviando email de recuperación: {str(e)}")
                # En desarrollo, retornar el token para pruebas
                if settings.DEBUG:
                    return Response({
                        'message': 'Email no pudo ser enviado, pero aquí está el token para pruebas',
                        'token': reset_token.token,
                        'reset_url': reset_url,
                    }, status=status.HTTP_200_OK)
                return Response({
                    'error': 'No se pudo enviar el email de recuperación'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'message': 'Email de recuperación enviado. Por favor, revisa tu correo.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        """Retornar información sobre el endpoint"""
        return Response({
            'endpoint': '/api/auth/password-reset/',
            'method': 'POST',
            'description': 'Solicitar recuperación de contraseña',
            'required_fields': ['email (string, registrado)'],
            'example': {'email': 'usuario@example.com'}
        })


class ConfirmPasswordResetAPIView(APIView):
    """
    API endpoint para confirmar recuperación de contraseña.
    
    Soporta múltiples formatos:
    - JSON: Content-Type: application/json
    - Form-data: Content-Type: application/x-www-form-urlencoded
    
    POST /api/auth/password-reset-confirm/
    {
        "token": "token_del_email",
        "password": "NuevaPass123!",
        "password2": "NuevaPass123!"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """Confirmar y procesar recuperación de contraseña"""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            reset_token = serializer.validated_data['reset_token']
            new_password = serializer.validated_data['password']
            
            # Actualizar contraseña
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Marcar token como usado
            reset_token.is_used = True
            reset_token.save()
            
            logger.info(f"Contraseña actualizada para usuario: {user.username}")
            
            return Response({
                'message': 'Contraseña actualizada exitosamente. Ya puedes iniciar sesión.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        """Retornar información sobre el endpoint"""
        return Response({
            'endpoint': '/api/auth/password-reset-confirm/',
            'method': 'POST',
            'description': 'Confirmar recuperación de contraseña',
            'required_fields': [
                'token (string, del email)',
                'password (string, nueva contraseña)',
                'password2 (string, confirmación)'
            ],
            'example': {
                'token': 'gAJ5y3Ht_xRqW2pL9vZm_dE5kFt7sB4cJ6gN...',
                'password': 'NuevaPass123!',
                'password2': 'NuevaPass123!'
            }
        })



