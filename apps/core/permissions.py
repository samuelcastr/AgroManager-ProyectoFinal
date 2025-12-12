from rest_framework import permissions
from apps.core.models import UserProfile


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
