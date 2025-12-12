# 🌾 AgroManager API — Backend Profesional con Django REST Framework

> Una API REST robusta, segura y escalable para gestión agrícola integral. Desarrollada con Django, JWT, filtrado avanzado y despliegue en producción.

**Versión:** 1.0.0  
**Estado:** En desarrollo  
**Equipo:** Proyecto Final — 4–6 integrantes  

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación Local](#instalación-local)
- [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
- [Ejecución Local](#ejecución-local)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Endpoints](#api-endpoints)
- [Autenticación JWT](#autenticación-jwt)
- [Filtrado Avanzado](#filtrado-avanzado)
- [Health Check](#health-check)
- [Tests Unitarios](#tests-unitarios)
- [Despliegue en Producción](#despliegue-en-producción)
- [Estructura Colaborativa](#estructura-colaborativa)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)

---

## ✨ Características

✅ **Arquitectura Profesional**
- Estructura modular con `config/` y `apps/`
- Separación de configuraciones: `dev.py` y `prod.py`
- DEBUG controlado por variables de entorno
- Seguridad robusta con HTTPS, HSTS, CSRF

✅ **Autenticación & Autorización**
- JWT con SimpleJWT (`access_token` y `refresh_token`)
- Permisos granulares personalizados
- Roles: Admin, Agricultor, Distribuidor, Técnico

✅ **API REST Completa**
- CRUD completo en cada app
- ModelSerializer con validaciones
- ViewSet + Router automático
- +2 endpoints personalizados por app

✅ **Filtrado Avanzado**
- Django-filter integrado
- Búsqueda case-insensitive
- Filtros por rango de fechas (gte, lte)
- Ordenamiento y paginación

✅ **Calidad de Código**
- Exception handler global personalizado
- Logging estructurado (consola y archivo)
- Transacciones atómicas para operaciones críticas
- Cobertura de tests >= 50%

✅ **Monitoreo & Operaciones**
- Health check anónimo (`/api/core/health/`)
- Sentry opcional para errores en producción
- Auditoría de cambios
- Documentación OpenAPI/Swagger

✅ **Base de Datos en la Nube**
- PostgreSQL, MySQL o SQLite (dev)
- Configuración dinámica via `DATABASE_URL`
- Migraciones automáticas

---

## 📦 Requisitos Previos

- **Python 3.12
- pip install --upgrade setuptools ( obligatorio en pruevas locales )
- **pip** (gestor de paquetes Python)
- **Git**
- **Base de datos en la nube** (PostgreSQL/MySQL) para producción
  - Recomendado: Supabase, Neon Tech, Railway, PlanetScale

**Opcional:**
- Docker (para despliegue)
- Sentry (para monitoreo de errores)

---

## 🚀 Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/samuelcastr/AgroManager-ProyectoFinal.git
cd AgroManager-ProyectoFinal
```

### 2. Crear y activar entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3.1 actualizar tools

```bash
pip install --upgrade setuptools
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus valores:

```dotenv
# Django
SECRET_KEY=tu-secret-key-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos (dev)
DATABASE_URL=sqlite:///db.sqlite3

# JWT
JWT_ACCESS_LIFETIME=60
JWT_REFRESH_LIFETIME=1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Sentry (opcional)
SENTRY_DSN=
```

### 5. Aplicar migraciones

```bash
python manage.py migrate --settings=config.settings.dev
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser --settings=config.settings.dev
```

---

## ⚙️ Configuración de Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```dotenv
# ========================================
# DJANGO CORE
# ========================================
SECRET_KEY=django-insecure-your-secret-key-here-CHANGE-IN-PRODUCTION
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=config.settings.dev

# ========================================
# DATABASE
# ========================================
# Dev (SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Producción (PostgreSQL via Supabase)
# DATABASE_URL=postgresql://user:password@host:5432/dbname

# Producción (MySQL via PlanetScale)
# DATABASE_URL=mysql://user:password@host:3306/dbname

# ========================================
# JWT TOKENS
# ========================================
JWT_ACCESS_LIFETIME=60
JWT_REFRESH_LIFETIME=1

# ========================================
# CORS & SECURITY
# ========================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
CSRF_TRUSTED_ORIGINS=http://localhost:8000

# Producción
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# ========================================
# EMAIL (OPCIONAL)
# ========================================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# ========================================
# MONITORING (OPCIONAL)
# ========================================
SENTRY_DSN=

# ========================================
# CELERY (OPCIONAL)
# ========================================
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

## 🏃 Ejecución Local

### Iniciar servidor de desarrollo

```bash
# Con settings de dev automáticamente
python manage.py runserver --settings=config.settings.dev

# O simplemente (si DJANGO_SETTINGS_MODULE está configurado)
python manage.py runserver
```

La API estará disponible en: **http://localhost:8000**

**Accesos importantes:**
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- Schema JSON: http://localhost:8000/swagger.json
- Admin: http://localhost:8000/admin/
- Health Check: http://localhost:8000/api/core/health/

---

## 📁 Estructura del Proyecto

```
AgroManager/
├── config/                    # Configuración central
│   ├── settings/
│   │   ├── base.py           # ⚙️ Configuración base
│   │   ├── dev.py            # 🔧 Desarrollo (DEBUG=True)
│   │   └── prod.py           # 🚀 Producción (DEBUG=False)
│   ├── urls.py               # URLs principales
│   ├── wsgi.py
│   ├── asgi.py
│   └── swagger.py            # Config OpenAPI
│
├── apps/                      # Aplicaciones del proyecto
│   ├── core/                  # 🔐 Núcleo (Samuel)
│   │   ├── models.py         # UserProfile, UnidadProductiva, AuditLog
│   │   ├── views.py          # Health check, ViewSets
│   │   ├── serializers.py    # Validación de datos
│   │   ├── permissions.py    # Permisos granulares
│   │   ├── exceptions.py     # Exception handler
│   │   ├── utils.py          # Utilidades
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── usuarios/              # 👤 Usuarios (Juan)
│   ├── inventario/            # 📦 Inventario (Beickert)
│   ├── cultivos/              # 🌾 Cultivos (María)
│   └── sensores/              # 📡 Sensores (Cielos)
│
├── manage.py
├── requirements.txt           # 📋 Dependencias
├── .env.example              # 🔑 Variables de entorno (ejemplo)
├── .gitignore
├── README.md                 # 📖 Este archivo
└── .github/
    └── workflows/
        └── ci.yml            # CI/CD Pipeline
```

---

## 🔌 API Endpoints

### Core (Autenticación y Base)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/core/health/` | Health check (anónimo) |
| `GET` | `/api/core/profiles/` | Listar perfiles de usuarios |
| `GET` | `/api/core/profiles/me/` | Obtener perfil del usuario logueado |
| `POST` | `/api/core/profiles/` | Crear perfil (admin) |
| `PUT` | `/api/core/profiles/{id}/` | Actualizar perfil |
| `DELETE` | `/api/core/profiles/{id}/` | Eliminar perfil |
| `GET` | `/api/core/unidades-productivas/` | Listar unidades productivas |
| `POST` | `/api/core/unidades-productivas/` | Crear unidad productiva |
| `GET` | `/api/core/unidades-productivas/{id}/cultivos/` | Cultivos de una unidad |

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/auth/login/` | Obtener `access_token` + `refresh_token` |
| `POST` | `/api/auth/refresh/` | Refrescar `access_token` |

---

## 🔐 Autenticación JWT

### 1. Login (obtener tokens)

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario","password":"contraseña"}'
```

**Respuesta:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Usar el token en requests

```bash
curl -X GET http://localhost:8000/api/core/profiles/ \
  -H "Authorization: Bearer <access_token>"
```

### 3. Refrescar token (cuando expire)

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh_token>"}'
```

**Tiempos de expiración (configurables):**
- `ACCESS_TOKEN_LIFETIME`: 60 minutos (dev)
- `REFRESH_TOKEN_LIFETIME`: 1 día (dev)

---

## 🔍 Filtrado Avanzado

### Búsqueda por nombre

```bash
GET /api/core/profiles/?search=juan
```

### Filtrar por rol

```bash
GET /api/core/profiles/?role=agricultor
```

### Filtrar por rango de fechas

```bash
GET /api/core/unidades-productivas/?created_at__gte=2025-01-01&created_at__lte=2025-03-01
```

### Combinaciones

```bash
GET /api/core/profiles/?role=agricultor&search=torres&is_verified=true
```

### Ordenamiento

```bash
GET /api/core/profiles/?ordering=-created_at
GET /api/core/profiles/?ordering=user__username
```

---

## 💚 Health Check

**Endpoint:** `GET /api/core/health/`  
**Permisos:** Anónimo (AllowAny)

### Respuesta exitosa (200 OK)

```json
{
  "status": "healthy",
  "timestamp": "2025-12-05T14:30:00.000Z",
  "server": "OK",
  "database": "OK"
}
```

### Respuesta con error de BD (503 Service Unavailable)

```json
{
  "status": "unhealthy",
  "timestamp": "2025-12-05T14:30:00.000Z",
  "server": "OK",
  "database": "ERROR"
}
```

**Uso en producción:**
- Plataformas lo usan para reiniciar la app
- Monitoreo externo (Uptime Robot, etc.)
- CI/CD pipelines

---

## 🧪 Tests Unitarios

### Ejecutar todos los tests

```bash
python manage.py test --settings=config.settings.dev
```

### Tests específicos

```bash
# Tests de core
python manage.py test apps.core.tests --settings=config.settings.dev

# Tests específicos
python manage.py test apps.core.tests.UserProfileSerializerTest --settings=config.settings.dev
```

### Con cobertura

```bash
coverage run --source='apps' manage.py test --settings=config.settings.dev
coverage report
coverage html  # genera reporte HTML
```

### Tests incluidos en core

- `UserProfileSerializer` (validación de teléfono y documento)
- `UnidadProductivaSerializer` (validación de coordenadas y área)
- `HealthCheckView` (estado del servidor y BD)
- Permisos (`IsOwner`, `IsAdminUser`, `IsAdminOrOwner`)
- Filtrado avanzado

---

## 🌐 Despliegue en Producción

### 1. Configurar variables de producción

```dotenv
# config/settings/prod.py variables
DEBUG=False
SECRET_KEY=tu-secret-key-super-segura
ALLOWED_HOSTS=api.tudominio.com
CSRF_TRUSTED_ORIGINS=https://api.tudominio.com

# Database (PostgreSQL en Supabase)
DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=noreply@tudominio.com
EMAIL_HOST_PASSWORD=tu-app-password

# Sentry (monitoreo de errores)
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

# Seguridad
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Crear Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear directorios necesarios
RUN mkdir -p logs

# Comandos de inicio
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "-w", "4"]
```

### 3. Desplegar en plataforma (Railway, Render, Fly.io)

**Railway:**
```bash
# Conectar repo
railway link
railway up
```

**Render:**
- Conectar GitHub
- Nueva Web Service
- Build command: `pip install -r requirements.txt && python manage.py migrate`
- Start command: `gunicorn config.wsgi:application`

**Fly.io:**
```bash
flyctl launch
flyctl secrets set SECRET_KEY=xxx
flyctl deploy
```

### 4. Post-despliegue

```bash
# Migraciones
python manage.py migrate --noinput --settings=config.settings.prod

# Static files
python manage.py collectstatic --noinput --settings=config.settings.prod

# Verificar health check
curl https://api.tudominio.com/api/core/health/
```

---

## 👥 Estructura Colaborativa

### Integrantes y Responsabilidades

| Integrante | App | Responsabilidad |
|-----------|-----|-----------------|
| **Samuel** | `core` | Autenticación, permisos, exception handler, deploy |
| **Juan** | `usuarios` | Usuarios, roles, JWT, login/logout |
| **Beickert** | `inventario` | Insumos, stock, transacciones atómicas |
| **María** | `cultivos` | Cultivos, ciclos, rendimiento |
| **Cielos** | `sensores` | Sensores, lecturas, reportes |

### Workflow Git

1. **Crear Issue** en GitHub
2. **Crear rama** desde `develop`: `juan/issue-12-usuarios-register`
3. **Hacer commits** con referencia: `feat(usuarios): implementar register #12`
4. **Crear PR** hacia `develop`
5. **Revisión cruzada** (mínimo 1 aprobación)
6. **Merge** a `develop`
7. **Samuel** hace merge final a `main`

---

## 🛠️ Tecnologías Utilizadas

- **Backend Framework:** Django 4.2 + Django REST Framework 3.14
- **Autenticación:** SimpleJWT 5.3 (JWT Bearer Tokens)
- **ORM:** Django ORM (con soporte PostgreSQL/MySQL/SQLite)
- **Validación:** DRF Serializers + django-filter
- **Documentación:** drf-yasg (OpenAPI/Swagger)
- **CORS:** django-cors-headers
- **Seguridad:** HTTPS, HSTS, CSRF Protection, Rate Limiting
- **Logging:** Python logging + Sentry (opcional)
- **Database:** PostgreSQL (prod) / SQLite (dev)
- **Server:** Gunicorn + Uvicorn (workers)
- **Despliegue:** Docker + Railway/Render/Fly.io

---

## 📞 Soporte & Contacto

- **Issues:** https://github.com/samuelcastr/AgroManager-ProyectoFinal/issues
- **Discussions:** https://github.com/samuelcastr/AgroManager-ProyectoFinal/discussions
- **Email:** samuel@example.com

---

## 📄 Licencia

Este proyecto está bajo licencia **MIT License**. Ver `LICENSE` para más detalles.

---

## 🙏 Agradecimientos

- Django REST Framework community
- SimpleJWT por autenticación JWT
- drf-yasg por OpenAPI/Swagger
- Equipo de desarrollo AgroManager

---

**Última actualización:** Diciembre 5, 2025  
**Versión:** 1.0.0-alpha

https://binding-honor-agromanager-b1a2d635.koyeb.app/api/auth/login/
