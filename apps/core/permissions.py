from rest_framework import permissions
from apps.core.models import UserProfile


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite:
    - Lectura a cualquier usuario
    - Escritura solo a administradores
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite:
    - Lectura a cualquier usuario
    - Escritura solo al propietario del objeto
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    Permiso que permite acceso solo al propietario del objeto
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user or request.user.is_staff
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff
        return False


class IsAdminUser(permissions.BasePermission):
    """
    Permiso que permite acceso solo a administradores
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsByRole(permissions.BasePermission):
    """
    Permiso que verifica el rol del usuario en UserProfile
    """
    required_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role in self.required_roles
        except UserProfile.DoesNotExist:
            return False


class IsAdmin(IsByRole):
    """Permiso para rol administrador"""
    required_roles = ['admin']


class IsAgricultor(IsByRole):
    """Permiso para rol agricultor"""
    required_roles = ['agricultor']


class IsDistribuidor(IsByRole):
    """Permiso para rol distribuidor"""
    required_roles = ['distribuidor']


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permite acceso solo a administradores o al propietario
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
