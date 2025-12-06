# 🔐 Ejemplos Prácticos - Autenticación AgroManager API

## Ejemplos en cURL

### 1. REGISTRO DE USUARIO

```bash
# Registrar un nuevo usuario agricultor
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "agricultor_beickert",
    "email": "beickert@agromanager.com",
    "password": "MiPassword123!",
    "password2": "MiPassword123!",
    "first_name": "Beickert",
    "last_name": "Martínez"
  }'

# Respuesta exitosa (201 Created):
# {
#   "message": "Usuario registrado exitosamente",
#   "user": {
#     "id": 2,
#     "username": "agricultor_beickert",
#     "email": "beickert@agromanager.com",
#     "first_name": "Beickert",
#     "last_name": "Martínez"
#   }
# }
```

---

### 2. LOGIN Y OBTENER TOKENS

```bash
# Login para obtener tokens
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "agricultor_beickert",
    "password": "MiPassword123!"
  }'

# Respuesta (200 OK):
# {
#   "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
# }

# Guardar los tokens para usar en requests posteriores
ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
REFRESH_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 3. USAR TOKEN EN REQUESTS AUTENTICADOS

```bash
# Ver perfil propio del usuario logueado
curl -X GET http://localhost:8000/api/core/profiles/me/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Listar todas las unidades productivas del usuario
curl -X GET http://localhost:8000/api/core/unidades-productivas/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Crear nueva unidad productiva
curl -X POST http://localhost:8000/api/core/unidades-productivas/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Finca Santa María",
    "description": "Cultivo de maíz y sorgo",
    "location": "Km 15 Vía a Bucaramanga",
    "latitude": 7.1256,
    "longitude": -73.1145,
    "area_hectareas": 25.5,
    "is_active": true
  }'
```

---

### 4. REFRESH TOKEN (Cuando expire el access)

```bash
# Obtener nuevo access token cuando expire
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "'$REFRESH_TOKEN'"
  }'

# Respuesta (200 OK):
# {
#   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
# }
```

---

### 5. RECUPERACIÓN DE CONTRASEÑA

#### Paso 1: Solicitar Recuperación

```bash
# Solicitar token de recuperación
curl -X POST http://localhost:8000/api/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "beickert@agromanager.com"}'

# Respuesta en DESARROLLO (retorna el token):
# {
#   "message": "Email no pudo ser enviado, pero aquí está el token para pruebas",
#   "token": "gAJ5y3Ht_xRqW2pL9vZm_dE5kFt7sB4cJ6gN...",
#   "reset_url": "http://localhost:3000/reset-password/gAJ5y3Ht_xRqW2pL9vZm_dE5kFt7sB4cJ6gN..."
# }

RESET_TOKEN="gAJ5y3Ht_xRqW2pL9vZm_dE5kFt7sB4cJ6gN..."
```

#### Paso 2: Confirmar Nueva Contraseña

```bash
# Confirmar recuperación con nueva contraseña
curl -X POST http://localhost:8000/api/auth/password-reset-confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "'$RESET_TOKEN'",
    "password": "NuevaPassword123!",
    "password2": "NuevaPassword123!"
  }'

# Respuesta (200 OK):
# {
#   "message": "Contraseña actualizada exitosamente. Ya puedes iniciar sesión."
# }
```

#### Paso 3: Login con Nueva Contraseña

```bash
# Ahora puedo login con la nueva contraseña
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "agricultor_beickert",
    "password": "NuevaPassword123!"
  }'
```

---

## Ejemplos en Python

### Script Completo de Registro y Login

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. REGISTRO
print("=" * 50)
print("1. REGISTRANDO NUEVO USUARIO")
print("=" * 50)

register_data = {
    "username": "maria_cultivos",
    "email": "maria@agromanager.com",
    "password": "MariaPass123!",
    "password2": "MariaPass123!",
    "first_name": "María",
    "last_name": "Soto"
}

response = requests.post(f"{BASE_URL}/api/auth/register/", json=register_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# 2. LOGIN
print("\n" + "=" * 50)
print("2. OBTENER TOKENS JWT")
print("=" * 50)

login_data = {
    "username": "maria_cultivos",
    "password": "MariaPass123!"
}

response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
tokens = response.json()
access_token = tokens['access']
refresh_token = tokens['refresh']

print(f"Status: {response.status_code}")
print(f"Access Token: {access_token[:50]}...")
print(f"Refresh Token: {refresh_token[:50]}...")

# 3. USAR TOKEN EN REQUEST
print("\n" + "=" * 50)
print("3. OBTENER PERFIL PROPIO")
print("=" * 50)

headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{BASE_URL}/api/core/profiles/me/", headers=headers)
print(f"Status: {response.status_code}")
print(f"Perfil: {json.dumps(response.json(), indent=2)}")

# 4. CREAR UNIDAD PRODUCTIVA
print("\n" + "=" * 50)
print("4. CREAR UNIDAD PRODUCTIVA")
print("=" * 50)

unidad_data = {
    "name": "Finca La Esperanza",
    "description": "Cultivo ecológico de hortalizas",
    "location": "Corregimiento de Lérida",
    "latitude": 5.5328,
    "longitude": -73.3565,
    "area_hectareas": 12.0,
    "is_active": True
}

response = requests.post(
    f"{BASE_URL}/api/core/unidades-productivas/",
    json=unidad_data,
    headers=headers
)
print(f"Status: {response.status_code}")
print(f"Unidad Creada: {json.dumps(response.json(), indent=2)}")

# 5. REFRESH TOKEN
print("\n" + "=" * 50)
print("5. REFRESH TOKEN")
print("=" * 50)

refresh_data = {"refresh": refresh_token}
response = requests.post(f"{BASE_URL}/api/auth/refresh/", json=refresh_data)
new_tokens = response.json()
new_access_token = new_tokens['access']

print(f"Status: {response.status_code}")
print(f"Nuevo Access Token: {new_access_token[:50]}...")
```

---

### Script de Recuperación de Contraseña

```python
import requests
import json
import time

BASE_URL = "http://localhost:8000"

# 1. SOLICITAR RECUPERACIÓN
print("=" * 50)
print("1. SOLICITAR RECUPERACIÓN DE CONTRASEÑA")
print("=" * 50)

reset_request = {"email": "maria@agromanager.com"}
response = requests.post(f"{BASE_URL}/api/auth/password-reset/", json=reset_request)
response_data = response.json()

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response_data, indent=2)}")

# En desarrollo, el token está en la respuesta
if 'token' in response_data:
    reset_token = response_data['token']
    print(f"\n✅ Token para pruebas: {reset_token}")
else:
    print("\n📧 Revisa tu email para obtener el token")
    reset_token = input("Ingresa el token del email: ")

# 2. CONFIRMAR RECUPERACIÓN
print("\n" + "=" * 50)
print("2. CONFIRMAR NUEVA CONTRASEÑA")
print("=" * 50)

confirm_data = {
    "token": reset_token,
    "password": "NuevaMariaPass123!",
    "password2": "NuevaMariaPass123!"
}

response = requests.post(
    f"{BASE_URL}/api/auth/password-reset-confirm/",
    json=confirm_data
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# 3. LOGIN CON NUEVA CONTRASEÑA
print("\n" + "=" * 50)
print("3. LOGIN CON NUEVA CONTRASEÑA")
print("=" * 50)

login_data = {
    "username": "maria_cultivos",
    "password": "NuevaMariaPass123!"
}

response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    print("\n✅ Contraseña actualizada exitosamente. ¡Bienvenido!")
```

---

### Clase Helper para Autenticación

```python
class AgroManagerAuth:
    """Helper para gestionar autenticación con AgroManager API"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        
    def register(self, username, email, password, first_name, last_name):
        """Registrar nuevo usuario"""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "password2": password,
            "first_name": first_name,
            "last_name": last_name
        }
        response = requests.post(f"{self.base_url}/api/auth/register/", json=data)
        return response.status_code == 201, response.json()
    
    def login(self, username, password):
        """Login y guardar tokens"""
        data = {"username": username, "password": password}
        response = requests.post(f"{self.base_url}/api/auth/login/", json=data)
        
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access']
            self.refresh_token = tokens['refresh']
            return True, "Login exitoso"
        return False, response.json()
    
    def request_password_reset(self, email):
        """Solicitar recuperación de contraseña"""
        data = {"email": email}
        response = requests.post(f"{self.base_url}/api/auth/password-reset/", json=data)
        return response.status_code == 200, response.json()
    
    def confirm_password_reset(self, token, new_password):
        """Confirmar nueva contraseña"""
        data = {
            "token": token,
            "password": new_password,
            "password2": new_password
        }
        response = requests.post(
            f"{self.base_url}/api/auth/password-reset-confirm/",
            json=data
        )
        return response.status_code == 200, response.json()
    
    def get_headers(self):
        """Obtener headers con token de autenticación"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def get_profile(self):
        """Obtener perfil del usuario actual"""
        response = requests.get(
            f"{self.base_url}/api/core/profiles/me/",
            headers=self.get_headers()
        )
        return response.status_code == 200, response.json()
    
    def create_unidad_productiva(self, name, location, latitude, longitude, area):
        """Crear nueva unidad productiva"""
        data = {
            "name": name,
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "area_hectareas": area,
            "is_active": True
        }
        response = requests.post(
            f"{self.base_url}/api/core/unidades-productivas/",
            json=data,
            headers=self.get_headers()
        )
        return response.status_code == 201, response.json()

# Uso:
if __name__ == "__main__":
    auth = AgroManagerAuth()
    
    # Registrar
    success, result = auth.register(
        "cielos_sensores",
        "cielos@agromanager.com",
        "CielosPass123!",
        "Cielos",
        "González"
    )
    print(f"Registro: {success} - {result}")
    
    # Login
    success, result = auth.login("cielos_sensores", "CielosPass123!")
    print(f"Login: {success} - {result}")
    
    # Obtener perfil
    success, profile = auth.get_profile()
    print(f"Perfil: {success} - {profile}")
    
    # Crear unidad productiva
    success, unidad = auth.create_unidad_productiva(
        "Parcela de Sensores",
        "Zona de pruebas IoT",
        5.52,
        -73.35,
        5.0
    )
    print(f"Unidad: {success} - {unidad}")
```

---

## Errores Comunes y Soluciones

### Error: "Las credenciales de autenticación no se proveyeron"
**Causa:** No incluyes el header `Authorization`  
**Solución:** Agrega `Authorization: Bearer <token>`

```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" http://localhost:8000/api/core/profiles/me/
```

---

### Error: "Token ha expirado"
**Causa:** El access token expiró (60 minutos)  
**Solución:** Usa el refresh token para obtener uno nuevo

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "'$REFRESH_TOKEN'"}'
```

---

### Error: "Contraseña debe contener..."
**Causa:** Contraseña no cumple requisitos  
**Requisitos:**
- Mínimo 8 caracteres
- Mayúsculas (A-Z)
- Minúsculas (a-z)
- Números (0-9)

**Ejemplo válido:** `SecurePass123!`

---

### Error: "Este email ya está registrado"
**Causa:** El email ya existe en la base de datos  
**Solución:** Usa otro email o recupera la contraseña si es tuya

---

## Testing Automático

```bash
# Ejecutar todos los tests
python manage.py test apps.core.tests --settings=config.settings.dev -v 2

# Solo tests de autenticación
python manage.py test apps.core.tests.RegisterAPITestCase --settings=config.settings.dev -v 2
python manage.py test apps.core.tests.PasswordResetAPITestCase --settings=config.settings.dev -v 2
```

---

**Última actualización:** 5 de diciembre de 2025  
**Versión:** 1.0

