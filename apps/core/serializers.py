from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from apps.core.models import UserProfile, UnidadProductiva, AuditLog, PasswordResetToken


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para UserProfile con validación completa"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone', 'role', 'document', 'bio', 'profile_picture', 'is_verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_phone(self, value):
        """Validar formato del teléfono"""
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo números, +, - y espacios.")
        return value

    def validate_document(self, value):
        """Validar documento único"""
        if value and UserProfile.objects.filter(document=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Este documento ya está registrado.")
        return value


class UnidadProductivaSerializer(serializers.ModelSerializer):
    """Serializer para UnidadProductiva"""
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = UnidadProductiva
        fields = ['id', 'name', 'description', 'owner', 'owner_username', 'location', 'latitude', 'longitude', 'area_hectareas', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def validate_area_hectareas(self, value):
        """Validar área positiva"""
        if value and value <= 0:
            raise serializers.ValidationError("El área debe ser mayor a cero.")
        return value

    def validate_latitude(self, value):
        """Validar rango de latitud"""
        if value and (value < -90 or value > 90):
            raise serializers.ValidationError("La latitud debe estar entre -90 y 90.")
        return value

    def validate_longitude(self, value):
        """Validar rango de longitud"""
        if value and (value < -180 or value > 180):
            raise serializers.ValidationError("La longitud debe estar entre -180 y 180.")
        return value


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer para AuditLog"""
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_username', 'action', 'model_name', 'object_id', 'old_values', 'new_values', 'ip_address', 'created_at']
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevo usuario"""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        help_text='Mínimo 8 caracteres con mayúscula, minúscula y número'
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}, 
        label='Confirmar contraseña',
        help_text='Debe coincidir exactamente con la contraseña anterior'
    )
    email = serializers.EmailField(required=True, help_text='Email válido y único')
    username = serializers.CharField(required=True, help_text='Nombre de usuario único')
    first_name = serializers.CharField(required=True, help_text='Tu nombre')
    last_name = serializers.CharField(required=True, help_text='Tu apellido')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_password(self, value):
        """Validar contraseña con validadores de Django"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate(self, data):
        """Validar que las contraseñas coincidan"""
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({'password2': 'Las contraseñas no coinciden.'})
        
        # Verificar email único
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({'email': 'Este email ya está registrado.'})
        
        # Verificar username único
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({'username': 'Este usuario ya existe.'})
        
        return data

    def create(self, validated_data):
        """Crear usuario y su perfil"""
        validated_data.pop('password2')  # Remover confirmación
        password = validated_data.pop('password')
        
        # Crear usuario
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Crear perfil automáticamente
        UserProfile.objects.create(user=user)
        
        return user


class RequestPasswordResetSerializer(serializers.Serializer):
    """Serializer para solicitar recuperación de contraseña"""
    email = serializers.EmailField()

    def validate_email(self, value):
        """Validar que el email exista"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('No existe usuario con este email.')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer para confirmar recuperación de contraseña"""
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirmar contraseña')

    def validate_password(self, value):
        """Validar contraseña"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate(self, data):
        """Validar token y contraseñas"""
        try:
            reset_token = PasswordResetToken.objects.get(token=data['token'])
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({'token': 'Token inválido.'})
        
        if not reset_token.is_valid():
            raise serializers.ValidationError({'token': 'El token ha expirado.'})
        
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({'password2': 'Las contraseñas no coinciden.'})
        
        data['reset_token'] = reset_token
        return data
