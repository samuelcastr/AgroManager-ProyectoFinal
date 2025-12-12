from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError

from .models import Cultivo, CicloSiembra
from .serializers import CultivoSerializer, CicloSerializer, CultivoFilterSet, CicloFilterSet


class CultivoViewSet(viewsets.ModelViewSet):
    permission_classes = []
    
    queryset = Cultivo.objects.all().order_by('-created_at')
    serializer_class = CultivoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CultivoFilterSet
    search_fields = ['nombre', 'tipo', 'variedad__nombre']
    ordering_fields = ['created_at', 'updated_at', 'nombre']

    def create(self, request, *args, **kwargs):
        """Crear cultivo con transacción atómica"""
        try:
            with transaction.atomic():
                return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Error al crear cultivo: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """Actualizar cultivo con transacción atómica"""
        try:
            with transaction.atomic():
                return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Error al actualizar cultivo: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """Eliminar cultivo con transacción atómica"""
        try:
            with transaction.atomic():
                return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': 'Error al eliminar cultivo: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def rendimiento_estimado(self, request, pk=None):
        """Obtener rendimiento promedio del cultivo"""
        try:
            cultivo = self.get_object()
            ciclos = cultivo.ciclos.all()
            total = 0
            count = 0
            for c in ciclos:
                if c.rendimiento_estimado is not None:
                    total += float(c.rendimiento_estimado)
                    count += 1
            promedio = total / count if count else None
            return Response({'cultivo': cultivo.nombre, 'rendimiento_promedio': promedio})
        except Cultivo.DoesNotExist:
            return Response({'error': 'Cultivo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Error al calcular rendimiento: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtener ciclos de siembra activos"""
        try:
            activos = CicloSiembra.objects.filter(estado=CicloSiembra.EN_PROGRESO)
            page = self.paginate_queryset(activos)
            serializer = CicloSerializer(page or activos, many=True)
            if page is not None:
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': 'Error al obtener ciclos activos: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CicloSiembraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar ciclos de siembra con transacciones atómicas
    y filtros avanzados (fecha, estado, cultivo, etc.)
    """
    permission_classes = []
    
    queryset = CicloSiembra.objects.all().order_by('-created_at')
    serializer_class = CicloSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CicloFilterSet
    search_fields = ['cultivo__nombre']
    ordering_fields = ['fecha_siembra', 'fecha_cosecha_estimada', 'created_at', 'estado']

    def create(self, request, *args, **kwargs):
        """Crear ciclo de siembra con transacción atómica"""
        try:
            with transaction.atomic():
                return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Error al crear ciclo: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """Actualizar ciclo de siembra con transacción atómica"""
        try:
            with transaction.atomic():
                return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Error al actualizar ciclo: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """Eliminar ciclo de siembra con transacción atómica"""
        try:
            with transaction.atomic():
                return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': 'Error al eliminar ciclo: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
