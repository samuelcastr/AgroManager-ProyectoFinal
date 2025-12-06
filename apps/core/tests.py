from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.core.models import UserProfile, UnidadProductiva, AuditLog, PasswordResetToken
from apps.core.serializers import UserProfileSerializer, UnidadProductivaSerializer


class HealthCheckTestCase(TestCase):
    """Tests para el endpoint de health check"""

    def setUp(self):
        self.client = Client()

    def test_health_check_returns_200(self):
        """Verificar que health check retorna 200 OK"""
        response = self.client.get('/api/core/health/')
        self.assertEqual(response.status_code, 200)

    def test_health_check_response_structure(self):
        """Verificar estructura de respuesta del health check"""
        response = self.client.get('/api/core/health/')
        data = response.json()
        
        self.assertIn('status', data)
        self.assertIn('timestamp', data)
        self.assertIn('server', data)
        self.assertIn('database', data)

    def test_health_check_is_anonymous(self):
        """Health check debe ser accesible sin autenticación"""
        # Sin login debería funcionar
        response = self.client.get('/api/core/health/')
        self.assertEqual(response.status_code, 200)


class UserProfileSerializerTestCase(TestCase):
    """Tests para UserProfileSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_user_profile_with_valid_phone(self):
        """Crear perfil con teléfono válido"""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='+57 3001234567',
            role='agricultor'
        )
        
        serializer = UserProfileSerializer(profile)
        self.assertEqual(serializer.data['phone'], '+57 3001234567')
        self.assertEqual(serializer.data['role'], 'agricultor')

    def test_validate_invalid_phone(self):
        """Validar rechazo de teléfono inválido"""
        data = {
            'phone': 'abc-123-xyz',
            'role': 'agricultor'
        }
        serializer = UserProfileSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_validate_unique_document(self):
        """Validar documento único"""
        profile1 = UserProfile.objects.create(
            user=self.user,
            document='1234567890',
            role='agricultor'
        )
        
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        data = {
            'document': '1234567890',
            'role': 'agricultor'
        }
        serializer = UserProfileSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_user_profile_string_representation(self):
        """Verificar representación en string del perfil"""
        profile = UserProfile.objects.create(
            user=self.user,
            role='admin'
        )
        self.assertIn('testuser', str(profile))
        self.assertIn('Administrador', str(profile))


class UnidadProductivaSerializerTestCase(TestCase):
    """Tests para UnidadProductivaSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_validate_area_positiva(self):
        """Validar que área debe ser positiva"""
        data = {
            'name': 'Mi Finca',
            'area_hectareas': -5,
        }
        serializer = UnidadProductivaSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_validate_latitude_range(self):
        """Validar rango de latitud"""
        data = {
            'name': 'Mi Finca',
            'latitude': 100,  # Fuera de rango [-90, 90]
        }
        serializer = UnidadProductivaSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_validate_longitude_range(self):
        """Validar rango de longitud"""
        data = {
            'name': 'Mi Finca',
            'longitude': -200,  # Fuera de rango [-180, 180]
        }
        serializer = UnidadProductivaSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_valid_unidad_productiva(self):
        """Crear unidad productiva válida"""
        unidad = UnidadProductiva.objects.create(
            name='Finca El Progreso',
            owner=self.user,
            location='Bogotá',
            latitude=4.7110,
            longitude=-74.0721,
            area_hectareas=50.0
        )
        
        serializer = UnidadProductivaSerializer(unidad)
        self.assertEqual(serializer.data['name'], 'Finca El Progreso')
        self.assertEqual(float(serializer.data['latitude']), 4.7110)


class UserProfileAPITestCase(APITestCase):
    """Tests para UserProfileViewSet API"""

    def setUp(self):
        self.client = APIClient()
        
        # Crear usuario y perfil
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='+57 3001234567',
            role='agricultor'
        )

    def test_list_profiles_requires_authentication(self):
        """Listar perfiles requiere autenticación"""
        response = self.client.get('/api/core/profiles/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_profiles_authenticated(self):
        """Listar perfiles con autenticación"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/core/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_own_profile_with_me_action(self):
        """Obtener perfil propio con endpoint /me/"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/core/profiles/me/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '+57 3001234567')

    def test_filter_profiles_by_role(self):
        """Filtrar perfiles por rol"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/core/profiles/?role=agricultor')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_search_profiles(self):
        """Buscar perfiles por nombre"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/core/profiles/?search=testuser')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_profile_requires_admin(self):
        """Crear perfil requiere ser admin"""
        self.client.force_authenticate(user=self.user)
        
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123'
        )
        
        data = {
            'user': new_user.id,
            'phone': '+57 3009876543',
            'role': 'distribuidor'
        }
        
        response = self.client.post('/api/core/profiles/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UnidadProductivaAPITestCase(APITestCase):
    """Tests para UnidadProductivaViewSet API"""

    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        self.unidad = UnidadProductiva.objects.create(
            name='Finca El Progreso',
            owner=self.user,
            location='Bogotá',
            area_hectareas=50.0,
            is_active=True
        )

    def test_list_unidades_authenticated(self):
        """Listar unidades requiere autenticación"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/core/unidades-productivas/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_only_see_own_unidades(self):
        """Usuario solo ve sus propias unidades"""
        # Crear unidad para otro usuario
        other_unidad = UnidadProductiva.objects.create(
            name='Finca Otra',
            owner=self.other_user,
            location='Medellín',
            area_hectareas=100.0
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/core/unidades-productivas/')
        
        # Solo debe ver su propia unidad
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Finca El Progreso')

    def test_create_unidad_auto_assigns_owner(self):
        """Crear unidad asigna automáticamente el propietario"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'Nueva Finca',
            'location': 'Cali',
            'area_hectareas': 30.0
        }
        
        response = self.client.post('/api/core/unidades-productivas/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.id)

    def test_filter_by_is_active(self):
        """Filtrar unidades por estado activo"""
        # Crear unidad inactiva
        inactive_unidad = UnidadProductiva.objects.create(
            name='Finca Inactiva',
            owner=self.user,
            is_active=False
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/core/unidades-productivas/?is_active=true')
        
        # Solo unidades activas
        active_count = len([u for u in response.data['results'] if u['is_active']])
        self.assertGreater(active_count, 0)


class TimestampedModelTestCase(TestCase):
    """Tests para campos de timestamp"""

    def test_timestamped_model_creates_timestamps(self):
        """Modelo timestamped crea created_at y updated_at"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        profile = UserProfile.objects.create(
            user=user,
            role='agricultor'
        )
        
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)
        self.assertEqual(profile.created_at, profile.updated_at)

    def test_updated_at_changes_on_update(self):
        """Updated_at se actualiza al modificar el objeto"""
        import time
        
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        profile = UserProfile.objects.create(
            user=user,
            role='agricultor'
        )
        
        created_at = profile.created_at
        
        time.sleep(0.1)
        
        profile.role = 'admin'
        profile.save()
        
        profile.refresh_from_db()
        
        self.assertEqual(profile.created_at, created_at)
        self.assertGreater(profile.updated_at, created_at)


class RegisterAPITestCase(APITestCase):
    """Tests para el endpoint de registro"""

    def test_register_user_success(self):
        """Registrar un usuario correctamente"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        
        # Verificar que se creó el usuario
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Verificar que se creó el perfil
        user = User.objects.get(username='newuser')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_register_user_passwords_mismatch(self):
        """Las contraseñas no coinciden"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password2': 'DifferentPassword123!',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_weak_password(self):
        """Contraseña muy débil"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': '123',
            'password2': '123',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_duplicate_username(self):
        """Nombre de usuario ya existe"""
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='password123'
        )
        data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetAPITestCase(APITestCase):
    """Tests para los endpoints de recuperación de contraseña"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPassword123!'
        )

    def test_request_password_reset(self):
        """Solicitar recuperación de contraseña"""
        data = {'email': 'test@example.com'}
        response = self.client.post('/api/auth/password-reset/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se creó el token
        self.assertTrue(PasswordResetToken.objects.filter(user=self.user).exists())

    def test_request_password_reset_invalid_email(self):
        """Email no registrado"""
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post('/api/auth/password-reset/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_confirm_password_reset_success(self):
        """Confirmar recuperación de contraseña correctamente"""
        # Crear token
        reset_token = PasswordResetToken.create_token(self.user)
        
        data = {
            'token': reset_token.token,
            'password': 'NewPassword123!',
            'password2': 'NewPassword123!',
        }
        response = self.client.post('/api/auth/password-reset-confirm/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el token está marcado como usado
        reset_token.refresh_from_db()
        self.assertTrue(reset_token.is_used)
        
        # Verificar que la contraseña cambió
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123!'))

    def test_confirm_password_reset_invalid_token(self):
        """Token inválido"""
        data = {
            'token': 'invalid_token_12345',
            'password': 'NewPassword123!',
            'password2': 'NewPassword123!',
        }
        response = self.client.post('/api/auth/password-reset-confirm/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_confirm_password_reset_passwords_mismatch(self):
        """Las contraseñas no coinciden"""
        reset_token = PasswordResetToken.create_token(self.user)
        
        data = {
            'token': reset_token.token,
            'password': 'NewPassword123!',
            'password2': 'DifferentPassword123!',
        }
        response = self.client.post('/api/auth/password-reset-confirm/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

