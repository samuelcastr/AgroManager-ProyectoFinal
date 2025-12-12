from rest_framework import permissions
from apps.core.models import UserProfile


# MAPEO DE ROLES A PERMISOS
ROLE_PERMISSIONS_MAP = {
    'admin': {
        'description': 'Administrador del sistema',
        'permissions': [
            'cultivos.list',
            'cultivos.create',
            'cultivos.update',
            'cultivos.delete',
            'inventario.list',
            'inventario.create',
            'inventario.update',
            'inventario.delete',
            'sensores.list',
            'sensores.create',
            'sensores.update',
            'sensores.delete',
            'usuarios.list',
            'usuarios.update',
        ]
    },
    'agricultor': {
        'description': 'Agricultor - Gestiona cultivos',
        'permissions': [
            'cultivos.list',       # Ver cultivos
            'cultivos.create',     # Crear cultivos
            'cultivos.update',     # Editar sus cultivos
            'cultivos.delete',     # Eliminar sus cultivos
            'sensores.list',       # Ver sensores
            'sensores.create',     # Crear sensores para cultivos
            'inventario.list',     # Ver inventario (lectura)
        ]
    },
    'distribuidor': {
        'description': 'Distribuidor - Gestiona inventario',
        'permissions': [
            'inventario.list',
            'inventario.create',
            'inventario.update',
            'inventario.delete',
            'sensores.list',       # Ver sensores
        ]
    },
    'tecnico': {
        'description': 'Tecnico - Gestiona sensores',
        'permissions': [
            'sensores.list',
            'sensores.create',
            'sensores.update',
            'sensores.delete',
            'sensores.read_realtime',
            'cultivos.list',       # Ver cultivos (lectura)
        ]
    },
    'usuario': {
        'description': 'Usuario regular - Acceso limitado',
        'permissions': [
            'cultivos.list',       # Solo lectura
            'inventario.list',     # Solo lectura
            'sensores.list',       # Solo lectura
        ]
    }
}


def get_role_permissions(role):
    """
    Obtener lista de permisos para un rol específico
    
    Args:
        role: El rol del usuario (admin, agricultor, etc.)
    
    Returns:
        dict con 'description' y 'permissions' list
    """
    return ROLE_PERMISSIONS_MAP.get(role, {'description': 'Sin rol', 'permissions': []})


class HasRolePermission(permissions.BasePermission):
    """
    Permiso personalizado que valida si el usuario tiene el permiso requerido
    basado en su rol.
    
    Uso en vistas:
        permission_classes = [IsAuthenticated, HasRolePermission]
        required_permission = 'cultivos.create'  # En la vista
    """
    
    def has_permission(self, request, view):
        """Verificar si el usuario tiene permiso para acceder a la vista"""
        # Obtener el usuario
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Obtener el rol del usuario
        try:
            profile = UserProfile.objects.get(user=request.user)
            role = profile.role
        except UserProfile.DoesNotExist:
            return False
        
        # Obtener los permisos requeridos de la vista
        required_permission = getattr(view, 'required_permission', None)
        
        # Si la vista no especifica permiso requerido, permitir
        if not required_permission:
            return True
        
        # Obtener los permisos del rol
        role_perms = get_role_permissions(role)
        permissions_list = role_perms.get('permissions', [])
        
        # Verificar si el usuario tiene el permiso
        return required_permission in permissions_list


def check_role_permission(permission_string):
    """
    Decorador que asigna el permiso requerido a una vista.
    
    Uso:
        @check_role_permission('cultivos.create')
        def post(self, request):
            ...
    """
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            # Obtener el usuario
            if not request.user or not request.user.is_authenticated:
                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {'detail': 'Requiere autenticacion'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Obtener el rol
            try:
                profile = UserProfile.objects.get(user=request.user)
                role = profile.role
            except UserProfile.DoesNotExist:
                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {'detail': 'Usuario sin rol asignado'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Verificar permiso
            role_perms = get_role_permissions(role)
            permissions_list = role_perms.get('permissions', [])
            
            if permission_string not in permissions_list:
                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {'detail': f'No tiene permiso para {permission_string}'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Permitir acceso
            return view_func(self, request, *args, **kwargs)
        
        return wrapper
    return decorator


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite:
    - Lectura a cualquier usuario autenticado
    - Escritura solo a administradores
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite:
    - Lectura a cualquier usuario autenticado
    - Escritura solo al propietario del objeto o admin
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return obj.owner == request.user or request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    Permiso que permite acceso solo al propietario del objeto o administrador
    Soporta objetos con campo 'owner' o 'user'
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False


class IsAdminUser(permissions.BasePermission):
    """
    Permiso que permite acceso solo a administradores del sistema
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permite acceso solo a administradores o al propietario del objeto
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


# ==================== PERMISOS POR ROL ====================

class BaseRolePermission(permissions.BasePermission):
    """
    Clase base para permisos por rol
    Los subclases deben definir 'allowed_roles'
    """
    allowed_roles = []
    allow_superuser = True

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Permitir a superusers
        if self.allow_superuser and request.user.is_staff:
            return True

        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role in self.allowed_roles
        except UserProfile.DoesNotExist:
            return False


class IsAdmin(BaseRolePermission):
    """Permiso para rol: administrador"""
    allowed_roles = ['admin']
    allow_superuser = True


class IsAgricultor(BaseRolePermission):
    """Permiso para rol: agricultor"""
    allowed_roles = ['agricultor']


class IsDistribuidor(BaseRolePermission):
    """Permiso para rol: distribuidor"""
    allowed_roles = ['distribuidor']


class IsTecnico(BaseRolePermission):
    """Permiso para rol: técnico"""
    allowed_roles = ['tecnico']


class IsUsuario(BaseRolePermission):
    """Permiso para rol: usuario regular"""
    allowed_roles = ['usuario']


class IsAgricultorOrTecnico(BaseRolePermission):
    """Permiso para roles: agricultor o técnico"""
    allowed_roles = ['agricultor', 'tecnico']


class IsAdminOrAgricultor(BaseRolePermission):
    """Permiso para roles: administrador o agricultor"""
    allowed_roles = ['admin', 'agricultor']


class IsDistribuidorOrAdmin(BaseRolePermission):
    """Permiso para roles: distribuidor o administrador"""
    allowed_roles = ['distribuidor', 'admin']


# ==================== PERMISOS COMBINADOS ====================

class IsAuthenticatedAndHasRole(permissions.IsAuthenticated):
    """
    Verifica que el usuario esté autenticado Y tenga un rol válido
    """
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.is_verified or request.user.is_staff
        except UserProfile.DoesNotExist:
            return False


class CanModifyOwnData(permissions.BasePermission):
    """
    Permiso que permite modificar solo sus propios datos
    Valida que el objeto sea del usuario actual
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if hasattr(obj, 'user'):
            return obj.user == request.user

        if hasattr(obj, 'owner'):
            return obj.owner == request.user

        return False


class CanViewOwnDataOrAdminCanViewAll(permissions.BasePermission):
    """
    Usuarios normales ven solo sus datos
    Admins ven todos los datos
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'user'):
                return obj.user == request.user
            if hasattr(obj, 'owner'):
                return obj.owner == request.user

        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
