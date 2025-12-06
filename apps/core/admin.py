from django.contrib import admin
from apps.core.models import UserProfile, UnidadProductiva, AuditLog, PasswordResetToken


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'role', 'phone', 'is_verified', 'created_at']
    list_filter = ['role', 'is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'document']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Usuario', {'fields': ('user',)}),
        ('Información Personal', {'fields': ('phone', 'document', 'bio', 'profile_picture')}),
        ('Rol y Permisos', {'fields': ('role', 'is_verified')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Nombre completo'


@admin.register(UnidadProductiva)
class UnidadProductivaAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'location', 'area_hectareas', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'owner']
    search_fields = ['name', 'description', 'location', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información General', {'fields': ('name', 'description', 'owner')}),
        ('Ubicación', {'fields': ('location', 'latitude', 'longitude')}),
        ('Área', {'fields': ('area_hectareas',)}),
        ('Estado', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'action', 'model_name', 'user', 'created_at']
    list_filter = ['action', 'model_name', 'created_at', 'user']
    search_fields = ['model_name', 'object_id', 'user__username']
    readonly_fields = ['created_at', 'user', 'action', 'model_name', 'object_id', 'old_values', 'new_values', 'ip_address', 'user_agent']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_valid', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['token', 'created_at', 'expires_at']

    def has_add_permission(self, request):
        return False

    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.short_description = 'Válido'
    is_valid.boolean = True

