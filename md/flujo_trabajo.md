# 🚀 WORKFLOW PROFESIONAL COMPLETO – AGROMANAGER API (versión ampliada con `core`)

---

# 👥 Integrantes y responsabilidades concretas (detallado)

* **Samuel Castro — Líder / Owner / App `core`**

  * Crea y configura el repo.
  * Protege ramas (main, develop).
  * Define estructura `config/`, settings y `prod/dev`.
  * Implementa `core` (autenticación, permisos globales, exception handler, logging, utilidades).
  * Configura CI/CD (GitHub Actions), despliegue y DB en la nube.
  * Revisa y hace merge final de PRs.
  * Construye health-check y documentación OpenAPI.
  * Responsable del deploy en producción.

* **Juan Riveros — App `usuarios`**

  * Models: perfiles, roles, permisos especiales.
  * JWT (SimpleJWT) y endpoints de login/logout/refresh.
  * Tests de login, permisos y endpoints de usuarios.
  * Filtros por nombre, email, fecha de creación.
  * Políticas de seguridad y rate limiting (si aplica).

* **Beickert Torres — App `inventario`**

  * Models: Insumo, Lote, MovimientoStock.
  * Operación atómica: creación de salida de stock + registro de movimiento.
  * Endpoints personalizados: alertas-stock, ajuste-masivo.
  * Tests de transacción y lógica de stock.

* **María Fernanda Rojas — App `cultivos`**

  * Models: Cultivo, CicloSiembra, Variedad.
  * Endpoints personalizados: rendimiento_estimado, ciclos_activos.
  * Relaciones: Cultivo → FK a UnidadProductiva (o Agricultor) → ManyToMany con Sensores.
  * Filtros por fechas, tipo, variedad y rendimiento.

* **Cielos Alexandra Rodríguez — App `sensores`**

  * Models: Sensor, LecturaSensor (timestamp, tipo, valor).
  * Endpoints: últimos-lecturas, reporte-intervalo (agrupado por día/hora).
  * Filtros por rango de fechas, tipo y rango de valores.
  * Integración con `cultivos` para alertas (e.g., humedad baja).

---

# 🌳 Estructura del repositorio (archivos y carpetas clave)

```
AgroManager/
├─ config/
│  ├─ settings/
│  │  ├─ base.py
│  │  ├─ dev.py
│  │  └─ prod.py
│  ├─ urls.py
│  └─ wsgi.py/ asgi.py
├─ apps/
│  ├─ core/
│  ├─ usuarios/
│  ├─ cultivos/
│  ├─ inventario/
│  └─ sensores/
├─ .env.example
├─ requirements.txt
├─ manage.py
├─ README.md
└─ .github/
   └─ workflows/
      └─ ci.yml
```

---

# 🧩 App `core` (Samuel) — **DETALLES COMPLETOS**

**Descripción:** `core` contiene todo lo compartido: user profile extension, base models, permisos globales, exception handler, utilidades, configuración JWT, logging, health check, y helpers para transacciones y filtros.

## Modelos (ejemplos)

* `TimestampedModel` (abstract): `created_at`, `updated_at`.
* `UserProfile` (OneToOne con `auth.User`): `phone`, `role`, `unit` (FK a UnidadProductiva si existiera).
* `UnidadProductiva` (puede residir aquí o en `cultivos` según diseño): `name`, `location`, `owner` FK a User.

## Serializers

* `BaseModelSerializer` (incluir validaciones comunes).
* `UserProfileSerializer` con validaciones (phone format).
* `UnidadProductivaSerializer`

## Views / Viewsets

* `HealthCheckView` (APIView):

  * GET `/health/`:

    * Verifica conexión DB: `from django.db import connections` + `connections['default'].cursor()`.
    * Verifica migrations pendientes opcional.
    * Respuesta 200 con JSON: `{server, database, timestamp}`.
* `UserProfileViewSet` (if exposed): router `/api/core/profiles/`.

## Permisos & Seguridad

* `IsAdminOrReadOnly` reutilizable.
* `CustomPermission` para verificaciones por rol (e.g., solo `manager` puede modificar ciertos recursos).

## Exception handler global

* `core.exceptions.custom_exception_handler` que haga:

  * Unificación de errores.
  * Logging (sentry o fallback).
  * Respuesta consistente con keys: `detail`, `code`, `errors`.

## Utilities

* `core.utils.send_email_async()`
* `core.utils.csv_export()`
* `core.constants` para choices.

## Configuración JWT y Settings

* `config/settings/base.py` importa `core` config.
* `core` incluye `SIMPLE_JWT` defaults en `base.py` y ajustes en `prod.py` (lifetimes).
* Variables en `.env`: `JWT_ACCESS_LIFETIME`, `JWT_REFRESH_LIFETIME`.

## Logging & Monitoring

* Logging config en `core.logging` con niveles por entorno.
* Sentry config opcional a partir de `SENTRY_DSN` en .env.

## Tests

* Tests unitarios para `UserProfileSerializer` y `HealthCheckView`.

---

# 📦 App `usuarios` (Juan) — **DETALLE TÉCNICO**

**Objetivo:** autenticación, usuarios, roles y permisos.

## Modelos

* `User` (usar `AUTH_USER_MODEL` si se extiende).
* `Role` (choice o model): `ADMIN`, `AGRICULTOR`, `DISTRIBUIDOR`.
* `FarmerProfile` (OneToOne con User) con `document`, `phone`, `address`.

Relaciones:

* `FarmerProfile` → `UnidadProductiva` (FK a `core.UnidadProductiva`).

## Serializers

* `UserSerializer` (create + update).
* `RegisterSerializer` con validaciones (password strength).
* `LoginSerializer` si se necesita endpoint custom.

## Views / Endpoints (mínimo 2 personalizados)

* Standard:

  * `UserViewSet` (ModelViewSet) – rutas `/api/usuarios/users/`.
* Personalizados:

  * `POST /api/usuarios/register/` → registrar con perfil.
  * `POST /api/usuarios/login/` → delega a SimpleJWT token obtain.
  * `GET /api/usuarios/me/` → datos del usuario logueado.
  * `GET /api/usuarios/roles/` → lista de roles (opcional).

## Permisos

* `IsAuthenticated` para endpoints sensibles.
* `IsAdminUser` para crear roles, listar users.

## Filters (django-filter + Search)

* `?search=name_or_email` (SearchFilter).
* `?date_joined__gte=2025-01-01`.
* `?role=AGRICULTOR`.

## Tests (mínimo)

* Registro exitoso y fallido (email duplicado).
* Login y refresh token.
* Acceso a `/me/` protegido.
* Permisos para endpoints admin.

## Ejemplo de Issue/Task para Juan

* Issue: “Implementar register + login con SimpleJWT #3”

  * Criterios: endpoints funcionales, tests >= 4, documentación Swagger.

---

# 🌾 App `cultivos` (María) — **DETALLE TÉCNICO**

**Objetivo:** CRUD de cultivos, ciclos, rendimiento y reportes.

## Modelos

* `Cultivo`

  * `id`, `name`, `tipo`, `variedad` (FK a `Variedad` o char), `unidad_productiva` FK a `core.UnidadProductiva`
* `CicloSiembra`

  * `cultivo` FK
  * `fecha_siembra`, `fecha_cosecha_estimada`, `estado` (EN_PROGRESO, FINALIZADO)
  * `superficie_hectareas`, `rendimiento_estimado`
* `Variedad` (opcional) con datos agronómicos.

Relaciones:

* `Cultivo` -> FK `unidad_productiva`.
* `CicloSiembra` -> FK `Cultivo`.
* Puede haber ManyToMany con `Sensor` para enlaces.

## Serializers

* `CultivoSerializer` (nested for ciclos optional).
* `CicloSerializer` con validación de fechas (fecha_siembra < fecha_cosecha).

## ViewSets & Endpoints personalizados

* `CultivoViewSet` (ModelViewSet):

  * CRUD estándar.
  * Custom action: `@action(detail=True, methods=['get'])` → `/api/cultivos/{pk}/rendimiento_estimado/`
  * Custom action: `/api/cultivos/activos/` → list ciclos activos.
* Router: `router.register('cultivos', CultivoViewSet)`

## Filtros

* `?name__icontains=maiz`
* `?fecha_siembra__gte=2025-01-01&fecha_siembra__lte=2025-03-01`
* `?variedad=HíbridaA`
* Búsqueda case-insensitive mediante `SearchFilter`.

## Transacciones atómicas

* Ejemplo: creación de `CicloSiembra` que crea registros paralelos y reserva insumos → envolver todo en `@transaction.atomic`.
* Caso de uso: cuando se confirma siembra se decrementa stock de insumos en INVENTARIO → operación cross-app que **debe** ser atómica.

## Tests

* Validación de creación de ciclo (fechas).
* Test del endpoint `rendimiento_estimado`.
* Test de filters (date range, name icontains).

---

# 🧾 App `inventario` (Beickert) — **DETALLE TÉCNICO + Transacción crítica**

**Objetivo:** manejar insumos, stock y movimientos.

## Modelos

* `Insumo`:

  * `name`, `sku`, `unidad_medida`, `categoria`.
* `Lote`:

  * `insumo` FK, `cantidad`, `fecha_vencimiento`, `ubicacion`.
* `MovimientoStock`:

  * `insumo` FK, `tipo` (INGRESO, SALIDA), `cantidad`, `referencia`, `created_by`
* `AjusteStock` (opcional) para auditoría.

## Serializers

* `InsumoSerializer`
* `MovimientoSerializer` con validación: si `SALIDA` comprobar stock suficiente.

## Endpoints personalizados (2+)

* `POST /api/inventario/ajustar-stock/`:

  * Request: `{insumo_id, cantidad, tipo, motivo}`
  * Lógica: crear `MovimientoStock` + actualizar `Lote` o `Insumo.total_stock`.
  * **Debe** estar dentro de `@transaction.atomic` para evitar inconsistencias.
* `GET /api/inventario/alertas-stock/`:

  * Devuelve insumos debajo de `min_stock`.

## Transacción ejemplo (código conceptual)

```python
from django.db import transaction

@api_view(['POST'])
def salida_stock(request):
    with transaction.atomic():
        # 1. validar stock
        # 2. crear MovimientoStock
        # 3. decrementar Lote(s)
        # 4. registrar auditoria
    return Response(...)
```

## Tests

* Simular concurrencia: dos requests de salida que potencialmente sobrepasen stock → asegurar que uno falla y rollback.
* Tests para alertas de stock.

---

# 📡 App `sensores` (Cielos) — **DETALLE TÉCNICO**

**Objetivo:** almacenar lecturas IoT y exponer reportes y filtros.

## Modelos

* `Sensor`:

  * `id`, `serial`, `tipo` (HUMEDAD, PH, TEMPERATURA), `ubicacion`, `cultivo` FK (opcional).
* `LecturaSensor`:

  * `sensor` FK, `timestamp` (indexed), `valor` (Decimal), `raw_payload` JSON.

Relaciones:

* `Sensor` → FK a `Cultivo` o a `UnidadProductiva`.

## Serializers

* `LecturaSerializer` con validaciones por `tipo` (rango permitido).
* Bulk serializer para ingesta masiva (si sensor envía lote).

## Endpoints personalizados (mínimo 2)

* `POST /api/sensores/lecturas/bulk/` → ingest batch readings.
* `GET /api/sensores/{id}/ultimas/` → últimas N lecturas.
* `GET /api/sensores/reporte/` → reporte agregado por día/hora:

  * params: `start`, `end`, `group_by=day|hour`.

## Filtros

* `?timestamp__gte=...&timestamp__lte=...`
* `?valor__gte=&valor__lte=`
* `?sensor__tipo=HUMEDAD`

## Alerta simple en endpoint

* Endpoint que devuelve cultivos con promedio humedad < threshold en últimos 24h.

## Tests

* Test de bulk ingest (rows corruptas → debe reportar fallos y sólo insertar correctas / o rollback según diseño).
* Test de reporte agregado (suma, avg, min, max).

---

# ✅ Reglas obligatorias y comprobaciones (resumen técnico)

* **Cada app**: CRUD completo, ModelSerializer, ViewSet+Router, 2 endpoints personalizados, 1 FK + 1 O2O o M2M mínima.
* **JWT SimpleJWT**: usado por `usuarios` y `core` config.
* **django-filter**: habilitado en settings y aplicado en ViewSets.
* **Exception handler global**: en `core` y referenciado en settings `REST_FRAMEWORK`.
* **Health check**: `/health/` en `core`.
* **DEBUG flag**: `dev.py` DEBUG=True, `prod.py` DEBUG=False. **main nunca debe tener DEBUG=True**.
* **DB en la nube**: configuración mediante `DATABASE_URL` en .env.
* **Tests**: cada app con tests para Models, Serializers, Views, Permisos. **Cobertura >= 50%**.
* **Transacción atómica**: al menos un endpoint cross-app (ej. confirmar siembra → reserva insumos en inventario) usando `@transaction.atomic`.

---

# 🔁 Flujo Git / Issues / Pull Requests (plantillas y requisitos)

## Issue template (mínimos campos)

* Título: `[APP] – Breve descripción`
* Descripción:

  * Objetivo
  * Pasos a realizar
  * Criterios de aceptación (tech)
  * Branch sugerida: `juan/issue-12-usuarios-register`
  * Responsable
  * Estimación (opcional)
* Checklist DoD:

  * Código pasa linters
  * Tests escritos
  * Documentación Swagger
  * README parcial actualizado

## Commit messages (estándar)

* `feat(app): brief description #issue`
* `fix(app): brief description #issue`
* `test(app): add tests for X #issue`

## PR template mínimo

* Título: `[APP Nombre] – Descripción breve`
* Referencia: `Closes #12`
* Descripción: qué se hizo y por qué.
* Checklist:

  * Issue referenciado
  * Tests añadidos y pasados
  * Documentación Swagger actualizada
  * Revisor asignado
  * Samuel debe estar como reviewer final
* Evidencia (screenshots, curl, ejemplos de requests/responses)

---

# 🧪 CI / GitHub Actions (recomendado por Samuel)

**Pipeline mínimo (`.github/workflows/ci.yml`):**

1. checkout
2. Setup Python
3. Install dependencies (`pip install -r requirements.txt`)
4. Lint (flake8/isort) — opcional pero recomendado
5. Run migrations on a temporary DB (sqlite or postgres service)
6. Run `python manage.py test`
7. Build Docker image (opcional)
8. Deploy step (solo en main y por Samuel; usar secrets)

**Protecciones en repo:**

* Branch protection: requieren PR review, passing CI, no force pushes.

---

# 🌐 Despliegue (pasos concretos para Samuel)

1. **Configurar variables de entorno en la plataforma elegida**

   * `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`, `SENTRY_DSN` (opcional), `JWT_*`, `DJANGO_SETTINGS_MODULE=config.settings.prod`
2. **Base de datos en la nube**

   * Crear instancia PostgreSQL (Railway/Supabase/Neon) y copiar `DATABASE_URL`.
3. **Dockerfile** (recomendado) con Gunicorn + Uvicorn workers

   * `CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker`
4. **Health check**

   * Configurar en la plataforma la URL `/health/`.
5. **Migrations**

   * Ejecutar `python manage.py migrate --noinput`.
6. **Collect static**

   * `python manage.py collectstatic --noinput`
7. **Verificar Swagger**

   * `/api/docs/` debe mostrar OpenAPI con todos los endpoints.
8. **Probar autenticación**

   * Obtener token via `/api/token/`, realizar llamada a endpoint protegido.
9. **Monitor**: revisar logs, configurar alertas básicas.

---

# 🧾 Documentación & README (qué incluir)

* Descripción del proyecto.
* Requisitos previos.
* Instrucciones locales:

  * `git clone ...`
  * `.env` variables y `.env.example`
  * `python -m venv .venv && pip install -r requirements.txt`
  * `python manage.py migrate`
  * `python manage.py runserver`
* Endpoints clave:

  * `/api/core/health/`
  * `/api/usuarios/`
  * `/api/cultivos/`
  * `/api/inventario/`
  * `/api/sensores/`
* Cómo ejecutar tests: `python manage.py test`
* Cómo desplegar (pasos resumidos)
* Region/URL de producción

---

# 🎯 Exposición final (script sugerido y división de 10 min)

* 0:00–0:30 — Intro por Samuel (problema + solución).
* 0:30–2:30 — Elevator pitch (equipo).
* 2:30–6:30 — Parte técnica (cada integrante 1:20):

  * Samuel: arquitectura, core, JWT, settings, CI/CD y deploy.
  * Juan: usuarios y seguridad (demostración login + /me).
  * María: cultivos (demo CRUD + rendimiento estimado).
  * Beickert: inventario (mostrar transacción atómica).
  * Cielos: sensores (demo reporte por intervalo).
* 6:30–9:30 — Código ajeno explicado (cada uno explica una parte que no escribió).
* 9:30–10:00 — Demo final: Swagger + llamada al health check y Q&A.

---

# ✅ Plantillas rápidas (copiables)

## Branch naming

```
<user>/<short-desc>-<issue#>
ej: maria/cultivos-crud-14
```

## Commit ejemplo

```
git commit -m "feat(cultivos): add CicloSiembra model & serializer #14"
```

## PR title ejemplo

```
[APP Cultivos] – CRUD CicloSiembra + endpoint rendimiento_estimado
```

