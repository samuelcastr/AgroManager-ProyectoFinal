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
    """Serializer para registro de nuevo usuario con rol y validación detallada"""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        help_text='Mínimo 8 caracteres, debe incluir mayúsculas, minúsculas, números y símbolos'
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}, 
        label='Confirmar contraseña',
        help_text='Debe coincidir exactamente con la contraseña anterior'
    )
    email = serializers.EmailField(required=True, help_text='Formato válido: usuario@dominio.com')
    role = serializers.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        required=True,
        help_text='Rol del usuario: admin, agricultor, distribuidor, tecnico, usuario'
    )
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Número de teléfono (formato: +XX XXXXXXXXXX)'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role', 'phone']
        extra_kwargs = {
            'username': {
                'required': True,
                'help_text': 'Solo letras, números y guiones bajos. Mínimo 3 caracteres.'
            },
            'first_name': {
                'required': True,
                'help_text': 'Tu nombre de pila'
            },
            'last_name': {
                'required': True,
                'help_text': 'Tu apellido'
            },
        }

    def validate_username(self, value):
        """Validar username"""
        if len(value) < 3:
            raise serializers.ValidationError('El usuario debe tener mínimo 3 caracteres.')
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError('El usuario solo puede contener letras, números y guiones bajos.')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Este nombre de usuario ya está registrado.')
        return value

    def validate_email(self, value):
        """Validar email"""
        if ';' in value or ',' in value:
            raise serializers.ValidationError('El email contiene caracteres inválidos. Use formato correcto: usuario@dominio.com')
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este email ya está registrado en el sistema.')
        return value

    def validate_first_name(self, value):
        """Validar nombre"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError('El nombre debe tener mínimo 2 caracteres.')
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError('El nombre solo puede contener letras y espacios.')
        return value.strip().title()

    def validate_last_name(self, value):
        """Validar apellido"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError('El apellido debe tener mínimo 2 caracteres.')
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError('El apellido solo puede contener letras y espacios.')
        return value.strip().title()

    def validate_phone(self, value):
        """Validar teléfono"""
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError('El teléfono debe contener solo números, +, - y espacios.')
        return value

    def validate_password(self, value):
        """Validar contraseña con mensajes claros"""
        errors = []
        
        if len(value) < 8:
            errors.append('Mínimo 8 caracteres (actual: {})'.format(len(value)))
        if not any(c.isupper() for c in value):
            errors.append('Debe incluir al menos una MAYÚSCULA')
        if not any(c.islower() for c in value):
            errors.append('Debe incluir al menos una minúscula')
        if not any(c.isdigit() for c in value):
            errors.append('Debe incluir al menos un NÚMERO (0-9)')
        
        special_chars = set('!@#$%^&*()_+-=[]{}|;:,.<>?')
        if not any(c in special_chars for c in value):
            errors.append('Debe incluir al menos un SÍMBOLO especial (!@#$%^&*etc)')
        
        if errors:
            raise serializers.ValidationError('Contraseña insegura: ' + '; '.join(errors))
        
        return value

    def validate(self, data):
        """Validar datos completos"""
        # Validar que las contraseñas coincidan
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({
                'password2': 'Las contraseñas no coinciden. Verifica que ambas sean idénticas.'
            })
        
        return data

    def create(self, validated_data):
        """Crear usuario y su perfil con rol especificado"""
        validated_data.pop('password2')  # Remover confirmación
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        phone = validated_data.pop('phone', None)
        
        # Crear usuario
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Crear perfil con rol automáticamente
        UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone
        )
        
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
