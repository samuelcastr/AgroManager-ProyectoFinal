from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets


class TimestampedModel(models.Model):
    """
    Modelo abstracto que proporciona campos de timestamps.
    Usado como base para todos los modelos que necesitan tracking de cambios.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")

    class Meta:
        abstract = True
        ordering = ['-updated_at']


class UserProfile(TimestampedModel):
    """
    Extensión del modelo User de Django.
    OneToOne con auth.User para agregar datos adicionales.
    """
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('agricultor', 'Agricultor'),
        ('distribuidor', 'Distribuidor'),
        ('tecnico', 'Técnico'),
        ('usuario', 'Usuario Regular'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='usuario', verbose_name="Rol")
    document = models.CharField(
        max_length=30, unique=True, blank=True, null=True,
        verbose_name="Documento de identidad"
    )
    bio = models.TextField(blank=True, null=True, verbose_name="Biografía")
    profile_picture = models.ImageField(
        upload_to='profiles/', blank=True, null=True,
        verbose_name="Foto de perfil"
    )
    is_verified = models.BooleanField(default=False, verbose_name="Verificado")

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['is_verified']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"


class UnidadProductiva(TimestampedModel):
    """
    Representa una unidad productiva agrícola.
    Puede estar asociada a uno o múltiples agricultores.
    """
    name = models.CharField(max_length=255, verbose_name="Nombre de la unidad")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unidades_productivas', verbose_name="Propietario")
    
    # Localización
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ubicación")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitud")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitud")
    
    # Área
    area_hectareas = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Área en hectáreas")
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Unidad productiva"
        verbose_name_plural = "Unidades productivas"
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class AuditLog(TimestampedModel):
    """
    Registro de auditoría para tracking de cambios en la API.
    """
    ACTION_CHOICES = [
        ('create', 'Crear'),
        ('update', 'Actualizar'),
        ('delete', 'Eliminar'),
        ('read', 'Leer'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Acción")
    model_name = models.CharField(max_length=100, verbose_name="Modelo afectado")
    object_id = models.CharField(max_length=100, verbose_name="ID del objeto")
    old_values = models.JSONField(blank=True, null=True, verbose_name="Valores anteriores")
    new_values = models.JSONField(blank=True, null=True, verbose_name="Valores nuevos")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Dirección IP")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")

    class Meta:
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Registros de auditoría"
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['model_name', 'action']),
        ]

    def __str__(self):
        return f"{self.action.upper()} {self.model_name} por {self.user} en {self.created_at}"


class PasswordResetToken(models.Model):
    """
    Tokens para recuperación de contraseña.
    Cada token es único y expira después de 24 horas.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='password_reset_token', verbose_name="Usuario")
    token = models.CharField(max_length=120, unique=True, db_index=True, verbose_name="Token")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    expires_at = models.DateTimeField(verbose_name="Expira en")
    is_used = models.BooleanField(default=False, verbose_name="Usado")

    class Meta:
        verbose_name = "Token de recuperación"
        verbose_name_plural = "Tokens de recuperación"

    def __str__(self):
        return f"Token para {self.user.email}"

    def is_valid(self):
        """Verificar si el token es válido (no expirado y no usado)"""
        return not self.is_used and timezone.now() <= self.expires_at

    @staticmethod
    def create_token(user):
        """Crear un nuevo token de recuperación para el usuario"""
        # Eliminar token anterior si existe
        PasswordResetToken.objects.filter(user=user).delete()
        
        # Crear nuevo token
        token = secrets.token_urlsafe(64)
        reset_token = PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        return reset_token

