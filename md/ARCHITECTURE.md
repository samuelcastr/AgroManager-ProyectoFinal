# 🏗️ Arquitectura de AgroManager API

## Visión General

AgroManager es una API REST profesional construida con **Django REST Framework** siguiendo patrones de arquitectura empresarial.

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENTES                            │
│  (Frontend, Mobile, Terceros, Swagger)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP(S)
                     │
┌────────────────────┴────────────────────────────────────────┐
│            CAPA DE ENRUTAMIENTO & MIDDLEWARE                │
│  (URLs, CORS, CSRF, Auth, Exception Handler)               │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    ┌───────────┬────────────┬──────────────┐
    │  Views   │ Viewsets  │ @api_view    │
    │          │ + Routers │ decorators   │
    └────┬─────┴────┬───────┴──────┬──────┘
         │          │              │
         └──────────┼──────────────┘
                    │
    ┌───────────────▼──────────────────┐
    │  SERIALIZERS (Validación)        │
    │  - UserProfileSerializer         │
    │  - UnidadProductivaSerializer    │
    └───────────────┬──────────────────┘
                    │
    ┌───────────────▼──────────────────┐
    │  PERMISOS (Authorization)        │
    │  - IsAdmin, IsOwner, etc         │
    └───────────────┬──────────────────┘
                    │
    ┌───────────────▼──────────────────┐
    │  MODELS (ORM)                    │
    │  - UserProfile, Unidad, etc      │
    └───────────────┬──────────────────┘
                    │
    ┌───────────────▼──────────────────┐
    │  DATABASE (PostgreSQL/MySQL)     │
    │  En la nube (Supabase, etc)      │
    └──────────────────────────────────┘
```

---

## 🎯 Principios de Diseño

### 1. **DRY (Don't Repeat Yourself)**
- Serializers reutilizables
- Permisos genéricos
- Utilidades compartidas en `core.utils`

### 2. **SOLID**
- **S**ingle Responsibility: Cada clase tiene una función clara
- **O**pen/Closed: Extensible sin modificar código existente
- **L**iskov Substitution: Herencia apropiada de permisos/serializers
- **I**nterface Segregation: Permisos específicos
- **D**ependency Inversion: Inyección de dependencias

### 3. **Seguridad por Defecto**
- DEBUG=False en producción
- SECRET_KEY desde env
- HTTPS forzado
- HSTS headers
- CSRF protection
- Rate limiting (opcional)

### 4. **Modularidad**
- Apps independientes
- Cada app es responsable de su dominio
- `core` es la base compartida

---

## 📦 Estructura de Apps

### `core/` (Fundación)

```
core/
├── models.py
│   ├── TimestampedModel (abstract)
│   ├── UserProfile (perfil extendido)
│   ├── UnidadProductiva (unidad de producción)
│   └── AuditLog (trazabilidad)
├── serializers.py
│   ├── UserProfileSerializer
│   ├── UnidadProductivaSerializer
│   └── AuditLogSerializer
├── views.py
│   ├── health() - endpoint anónimo
│   ├── UserProfileViewSet
│   ├── UnidadProductivaViewSet
│   └── AuditLogViewSet
├── permissions.py
│   ├── IsAdminUser
│   ├── IsOwner
│   ├── IsByRole
│   └── IsAdminOrOwner
├── exceptions.py
│   ├── custom_exception_handler
│   └── Exception classes
├── utils.py
│   ├── atomic_transaction (transacciones)
│   ├── send_email_async
│   ├── export_to_csv
│   └── helpers
└── urls.py (router automático)
```

**Responsabilidades:**
- Autenticación JWT
- Extensión de User
- Permisos globales
- Exception handling
- Utilidades compartidas
- Health check
- Auditoría

### Otras Apps

```
usuarios/    # Gestión de usuarios y roles
inventario/  # Control de insumos y stock
cultivos/    # Gestión de cultivos
sensores/    # Lecturas de sensores IoT
```

---

## 🔄 Flujo de una Solicitud HTTP

```
1. REQUEST llega a Django
   ↓
2. URL Router (/api/core/profiles/)
   ↓
3. MIDDLEWARE
   - CorsMiddleware
   - SessionMiddleware
   - SecurityMiddleware
   ↓
4. VIEW / VIEWSET
   - Verificar permisos
   ↓
5. SERIALIZER
   - Validar entrada (POST/PUT)
   ↓
6. MODELS
   - Query a BD
   - Lógica de negocio
   ↓
7. RESPONSE
   - Serializar output
   - JSON response
   ↓
8. Exception Handler (si hay error)
   - Loguear
   - Formatear error
   - Retornar response uniforme
```

---

## 🔐 Autenticación & Autorización

### JWT Flow

```
1. Cliente hace login
   POST /api/auth/login/
   {"username": "user", "password": "pass"}
   
2. Server retorna tokens
   {
     "access": "eyJ...",     # Expira en 60 min
     "refresh": "eyJ..."     # Expira en 1 día
   }

3. Cliente incluye token en requests
   Authorization: Bearer <access_token>

4. Cuando access expira
   POST /api/auth/refresh/
   {"refresh": "<refresh_token>"}
   → Nuevo access_token
```

### Niveles de Permiso

```
┌─────────────────────────────────────┐
│  IsAuthenticated (JWT válido)      │
│  Nivel: Usuario logueado           │
├─────────────────────────────────────┤
│  IsAdminUser (es staff)            │
│  Nivel: Administrador              │
├─────────────────────────────────────┤
│  IsOwner (propietario del recurso) │
│  Nivel: Propietario                │
├─────────────────────────────────────┤
│  IsByRole (rol en UserProfile)     │
│  Nivel: Agricultor, Distribuidor   │
├─────────────────────────────────────┤
│  IsAdminOrReadOnly (SAFE_METHODS)  │
│  Nivel: Lectura libre, admin puede escribir
├─────────────────────────────────────┤
│  AllowAny (sin restricción)         │
│  Nivel: Público (health check)     │
└─────────────────────────────────────┘
```

---

## 📊 Modelos & Relaciones

### User Profile Extension

```
User (Django Auth)
  │
  └──OneToOne──UserProfile
              ├── role (choices)
              ├── phone
              ├── document (unique)
              ├── bio
              └── profile_picture
```

### Unidades Productivas

```
User (propietario)
  │
  └──ForeignKey──UnidadProductiva
                 ├── location
                 ├── coordinates (lat/lng)
                 ├── area_hectareas
                 └── cultivos (integración)
```

### Auditoría

```
User (quién hizo cambio)
  │
  └──ForeignKey──AuditLog
                 ├── action (create/update/delete)
                 ├── model_name
                 ├── object_id
                 ├── old_values (JSON)
                 └── new_values (JSON)
```

---

## 🔍 Filtrado Avanzado

**Configuración en `settings/base.py`:**

```python
"DEFAULT_FILTER_BACKENDS": [
    "django_filters.rest_framework.DjangoFilterBackend",
    "rest_framework.filters.SearchFilter",
    "rest_framework.filters.OrderingFilter",
]
```

**ViewSet example:**

```python
class UserProfileViewSet(viewsets.ModelViewSet):
    filterset_fields = ['role', 'is_verified']
    search_fields = ['user__username', 'user__email', 'phone']
    ordering_fields = ['created_at', 'user__username']
```

**Queries disponibles:**

```
GET /api/core/profiles/?role=agricultor
GET /api/core/profiles/?search=juan
GET /api/core/profiles/?is_verified=true
GET /api/core/profiles/?created_at__gte=2025-01-01
GET /api/core/profiles/?ordering=-updated_at
```

---

## ⚡ Transacciones Atómicas

**Caso de uso:** Cuando se confirma una siembra, se deben:
1. Crear registro en `cultivos.CicloSiembra`
2. Decrementar stock en `inventario.Lote`
3. Registrar movimiento en `inventario.MovimientoStock`

**Si falla cualquiera → rollback de todo**

```python
from django.db import transaction

@transaction.atomic
def confirmar_siembra(request):
    # 1. Crear ciclo
    ciclo = CicloSiembra.objects.create(...)
    
    # 2. Decrementar stock
    lote = Lote.objects.select_for_update().get(id=...)
    lote.cantidad -= cantidad
    lote.save()
    
    # 3. Registrar movimiento
    MovimientoStock.objects.create(...)
    
    # Si hay error → rollback automático
    return ciclo
```

---

## 🎯 Exception Handling

**Sin personalización:**
```json
{
  "detail": [
    "This field is required."
  ]
}
```

**Con personalización (`custom_exception_handler`):**
```json
{
  "detail": "Validation failed",
  "code": "validation_error",
  "errors": {
    "phone": ["Invalid phone format"],
    "email": ["Already exists"]
  }
}
```

---

## 📝 Logging

**Niveles:**
- `DEBUG`: Desarrollo (verbose)
- `INFO`: Información importante
- `WARNING`: Advertencias
- `ERROR`: Errores capturados
- `CRITICAL`: Errores no recuperables

**Destinos:**
- Console (desarrollo)
- Archivo rotativo (producción)
- Sentry (opcional, errores críticos)

---

## 🧪 Testing Strategy

```
┌─────────────────────────────┐
│  Unit Tests                 │
│  - Serializers validación   │
│  - Permisos                 │
│  - Utils                    │
├─────────────────────────────┤
│  Integration Tests          │
│  - ViewSet completo         │
│  - Filtrado                 │
│  - Transacciones            │
├─────────────────────────────┤
│  API Tests                  │
│  - Endpoints                │
│  - Auth flow                │
│  - Error handling           │
└─────────────────────────────┘
```

**Cobertura objetivo:** >= 50%

```bash
coverage run --source='apps' manage.py test
coverage report
```

---

## 🚀 Despliegue

### Desarrollo
- `DEBUG=True`
- SQLite (local)
- Email a console
- Swagger completo

### Producción
- `DEBUG=False` ✅ OBLIGATORIO
- PostgreSQL en la nube
- Email SMTP
- Sentry habilitado
- HTTPS + HSTS
- Gunicorn + 4 workers
- Static files en CDN

---

## 📈 Escalabilidad

### Mejoras futuras

1. **Caché**
   - Redis para sesiones
   - Cache de permisos

2. **Celery**
   - Tareas asincrónicas
   - Envío de emails en background
   - Reportes

3. **API Gateway**
   - Rate limiting
   - Throttling

4. **Microservicios**
   - Separar apps por servicio
   - Comunicación via APIs

5. **Analytics**
   - Dashboards
   - Reportes avanzados

---

## 📚 Referencias

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT](https://github.com/jpadilla/django-rest-framework-simplejwt)
- [django-filter](https://django-filter.readthedocs.io/)

