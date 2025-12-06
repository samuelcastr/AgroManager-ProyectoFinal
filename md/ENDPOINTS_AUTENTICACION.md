# Endpoints de Autenticación - AgroManager API

## Descripción General

Estos endpoints proporcionan funcionalidades completas de autenticación incluyendo:
- ✅ Registro de nuevos usuarios
- ✅ Login con JWT
- ✅ Recuperación de contraseña
- ✅ Refresh de tokens

---

## 1. Registro de Usuario

### Endpoint
```
POST /api/auth/register/
```

### Descripción
Registra un nuevo usuario en el sistema y crea automáticamente su perfil.

### Autenticación
No requerida (público)

### Parámetros (Body JSON)

| Campo | Tipo | Requerido | Descripción |
|-------|------|----------|-------------|
| `username` | string | Sí | Nombre de usuario único (2-150 caracteres) |
| `email` | string | Sí | Email único y válido |
| `password` | string | Sí | Contraseña (mín. 8 caracteres, debe incluir mayúsculas, minúsculas y números) |
| `password2` | string | Sí | Confirmación de contraseña (debe coincidir con `password`) |
| `first_name` | string | Sí | Nombre del usuario |
| `last_name` | string | Sí | Apellido del usuario |

### Ejemplo de Solicitud

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_agricola",
    "email": "juan@agromanager.com",
    "password": "AgroPassword123!",
    "password2": "AgroPassword123!",
    "first_name": "Juan",
    "last_name": "García"
  }'
```

### Respuesta Exitosa (201 Created)

```json
{
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 2,
    "username": "juan_agricola",
    "email": "juan@agromanager.com",
    "first_name": "Juan",
    "last_name": "García"
  }
}
```

### Errores Posibles

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| 400 | Contraseñas no coinciden | `{"password2": ["Las contraseñas no coinciden."]}` |
| 400 | Contraseña débil | `{"password": ["Esta contraseña es muy corta..."]}` |
| 400 | Username ya existe | `{"username": ["Este usuario ya existe."]}` |
| 400 | Email ya existe | `{"email": ["Este email ya está registrado."]}` |

---

## 2. Login (Obtener Token JWT)

### Endpoint
```
POST /api/auth/login/
```

### Descripción
Autentica el usuario y devuelve tokens JWT (access y refresh).

### Autenticación
No requerida (público)

### Parámetros (Body JSON)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `username` | string | Nombre de usuario registrado |
| `password` | string | Contraseña del usuario |

### Ejemplo de Solicitud

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_agricola",
    "password": "AgroPassword123!"
  }'
```

### Respuesta Exitosa (200 OK)

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Tiempos de Expiración:**
- `access`: 60 minutos
- `refresh`: 24 horas

### Errores Posibles

| Código | Descripción |
|--------|-------------|
| 401 | Credenciales inválidas |

---

## 3. Refresh de Token

### Endpoint
```
POST /api/auth/refresh/
```

### Descripción
Genera un nuevo token `access` usando el token `refresh`.

### Autenticación
No requerida (público)

### Parámetros (Body JSON)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `refresh` | string | Token refresh recibido en login |

### Ejemplo de Solicitud

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

### Respuesta Exitosa (200 OK)

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 4. Solicitar Recuperación de Contraseña

### Endpoint
```
POST /api/auth/password-reset/
```

### Descripción
Solicita un token de recuperación y envía un email al usuario (en desarrollo muestra el token).

### Autenticación
No requerida (público)

### Parámetros (Body JSON)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `email` | string | Email registrado en el sistema |

### Ejemplo de Solicitud

```bash
curl -X POST http://localhost:8000/api/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@agromanager.com"
  }'
```

### Respuesta Exitosa (200 OK)

**Producción:** (solo mensaje)
```json
{
  "message": "Email de recuperación enviado. Por favor, revisa tu correo."
}
```

**Desarrollo:** (retorna el token para pruebas)
```json
{
  "message": "Email no pudo ser enviado, pero aquí está el token para pruebas",
  "token": "gAJ5y3Ht_xRqW2pL9vZm_dE5kFt7sB4cJ6gN...",
  "reset_url": "http://localhost:3000/reset-password/gAJ5y3Ht_xRqW2pL9vZm_dE5kFt7sB4cJ6gN..."
}
```

### Errores Posibles

| Código | Descripción |
|--------|-------------|
| 400 | Email no registrado |

### Notas
- El token expira en **24 horas**
- En desarrollo, el token se retorna en la respuesta para pruebas
- En producción, se envía solo a través de email

---

## 5. Confirmar Recuperación de Contraseña

### Endpoint
```
POST /api/auth/password-reset-confirm/
```

### Descripción
Confirma la recuperación de contraseña usando el token y establece una nueva contraseña.

### Autenticación
No requerida (público)

### Parámetros (Body JSON)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `token` | string | Token recibido en el email |
| `password` | string | Nueva contraseña |
| `password2` | string | Confirmación de nueva contraseña |

### Ejemplo de Solicitud

```bash
curl -X POST http://localhost:8000/api/auth/password-reset-confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "gAJ5y3Ht_xRqW2pL9vZm_dE5kFt7sB4cJ6gN...",
    "password": "NuevaPassword123!",
    "password2": "NuevaPassword123!"
  }'
```

### Respuesta Exitosa (200 OK)

```json
{
  "message": "Contraseña actualizada exitosamente. Ya puedes iniciar sesión."
}
```

### Errores Posibles

| Código | Descripción |
|--------|-------------|
| 400 | Token inválido |
| 400 | Token expirado (> 24 horas) |
| 400 | Token ya fue usado |
| 400 | Contraseñas no coinciden |
| 400 | Contraseña débil |

---

## Ejemplo de Flujo Completo

### 1. Registro
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mariajose",
    "email": "maria@agromanager.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "María",
    "last_name": "Soto"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mariajose",
    "password": "SecurePass123!"
  }'
```
Guarda el `access` token para requests autenticados.

### 3. Usar token en requests
```bash
curl -X GET http://localhost:8000/api/core/profiles/me/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. Refresh token cuando expire
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

### 5. Recuperar contraseña olvidada
```bash
# Solicitar recuperación
curl -X POST http://localhost:8000/api/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "maria@agromanager.com"}'

# Confirmar recuperación (con token del email)
curl -X POST http://localhost:8000/api/auth/password-reset-confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "token_from_email",
    "password": "NuevaPassword123!",
    "password2": "NuevaPassword123!"
  }'
```

---

## Requisitos de Contraseña

Las contraseñas deben cumplir estos requisitos:

- ✅ Mínimo 8 caracteres
- ✅ Contener al menos una mayúscula
- ✅ Contener al menos una minúscula
- ✅ Contener al menos un número
- ✅ No ser completamente numérica
- ✅ No ser una contraseña común

---

## Documentación Interactiva

Accede a la documentación interactiva en:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

Prueba todos los endpoints directamente desde la interfaz.

---

## Notas de Desarrollo

### Email en Desarrollo
- Los emails se envían a la consola con `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
- El token se retorna en la respuesta de `password-reset/` para pruebas

### Email en Producción
- Configura `EMAIL_BACKEND` con tu proveedor (SendGrid, AWS SES, etc.)
- Configura `FRONTEND_URL` en settings para generar el enlace correcto
- Los tokens se envían solo por email

### Pruebas
Ejecuta los tests:
```bash
python manage.py test apps.core.tests.RegisterAPITestCase --settings=config.settings.dev
python manage.py test apps.core.tests.PasswordResetAPITestCase --settings=config.settings.dev
```

---

**Última actualización:** 5 de diciembre de 2025  
**Versión:** 1.0
