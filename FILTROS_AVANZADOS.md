# Documentación de Filtros Avanzados - AgroManager

## Transacciones Atómicas

Se implementó transacciones atómicas en todas las operaciones críticas usando `@transaction.atomic()`:

```python
from django.db import transaction

with transaction.atomic():
    # Operación crítica que debe ejecutarse completamente o no ejecutarse
```

**Operaciones con transacciones:**
- `CultivoViewSet.create()` - Crear cultivo
- `CultivoViewSet.update()` - Actualizar cultivo
- `CultivoViewSet.destroy()` - Eliminar cultivo
- `CicloSiembraViewSet.create()` - Crear ciclo de siembra
- `CicloSiembraViewSet.update()` - Actualizar ciclo
- `CicloSiembraViewSet.destroy()` - Eliminar ciclo

---

## Manejo Global de Errores

Se implementó un manejador global de excepciones que captura y formatea errores HTTP:

**Códigos de error manejados:**
- `400` Bad Request - Solicitud inválida
- `401` Unauthorized - No autorizado
- `403` Forbidden - Prohibido
- `404` Not Found - No encontrado
- `405` Method Not Allowed - Método no permitido
- `500` Internal Server Error - Error interno

**Archivo:** `cultivos/exception_handler.py`

**Respuesta de error estándar:**
```json
{
  "success": false,
  "status_code": 400,
  "error": {
    "type": "ValidationError",
    "message": "Error al validar los datos",
    "details": { }
  }
}
```

---

## Filtros Avanzados

### 1. Filtros para Cultivos

**Endpoint:** `GET /api/cultivos/`

#### Parámetros disponibles:

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `nombre` | string | Búsqueda case-insensitive en nombre | `?nombre=trigo` |
| `tipo` | string | Búsqueda case-insensitive en tipo | `?tipo=cereal` |
| `variedad` | string | Búsqueda en nombre de variedad | `?variedad=blanca` |
| `unidad_productiva` | string | Búsqueda en unidad productiva | `?unidad_productiva=campo_norte` |
| `fecha_inicio_after` | date | Fecha desde (creación) | `?fecha_inicio_after=2024-01-01` |
| `fecha_inicio_before` | date | Fecha hasta (creación) | `?fecha_inicio_before=2024-12-31` |
| `search` | string | Búsqueda en nombre, tipo, variedad | `?search=arroz` |
| `ordering` | string | Ordenar por campo | `?ordering=-created_at` |

#### Ejemplos de uso:

```bash
# Búsqueda simple por nombre
curl "http://localhost:8000/api/cultivos/?nombre=trigo"

# Búsqueda case-insensitive
curl "http://localhost:8000/api/cultivos/?nombre_icontains=TRIGO"

# Búsqueda por tipo de cultivo
curl "http://localhost:8000/api/cultivos/?tipo=cereal"

# Búsqueda por variedad
curl "http://localhost:8000/api/cultivos/?variedad=blanca"

# Filtro de rango de fechas
curl "http://localhost:8000/api/cultivos/?fecha_inicio_after=2024-01-01&fecha_inicio_before=2024-12-31"

# Múltiples filtros combinados
curl "http://localhost:8000/api/cultivos/?nombre=trigo&tipo=cereal&variedad=blanca"

# Búsqueda general y ordenamiento
curl "http://localhost:8000/api/cultivos/?search=arroz&ordering=-created_at"

# Ordenar ascendente por nombre
curl "http://localhost:8000/api/cultivos/?ordering=nombre"
```

---

### 2. Filtros para Ciclos de Siembra

**Endpoint:** `GET /api/ciclos/`

#### Parámetros disponibles:

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `cultivo__nombre` | string | Nombre del cultivo (icontains) | `?cultivo__nombre=maíz` |
| `estado` | choice | Estado (EN_PROGRESO, FINALIZADO) | `?estado=EN_PROGRESO` |
| `fecha_siembra_inicio` | date | Fecha siembra desde (>=) | `?fecha_siembra_inicio=2024-01-01` |
| `fecha_siembra_fin` | date | Fecha siembra hasta (<=) | `?fecha_siembra_fin=2024-12-31` |
| `fecha_cosecha_inicio` | date | Fecha cosecha desde (>=) | `?fecha_cosecha_inicio=2024-06-01` |
| `fecha_cosecha_fin` | date | Fecha cosecha hasta (<=) | `?fecha_cosecha_fin=2024-12-31` |
| `search` | string | Búsqueda en nombre del cultivo | `?search=maíz` |
| `ordering` | string | Ordenar por campo | `?ordering=-fecha_siembra` |

#### Ejemplos de uso:

```bash
# Filtrar ciclos activos
curl "http://localhost:8000/api/ciclos/?estado=EN_PROGRESO"

# Filtrar por nombre de cultivo
curl "http://localhost:8000/api/ciclos/?cultivo__nombre=maíz"

# Rango de fechas de siembra
curl "http://localhost:8000/api/ciclos/?fecha_siembra_inicio=2024-01-01&fecha_siembra_fin=2024-12-31"

# Rango de fechas de cosecha estimada
curl "http://localhost:8000/api/ciclos/?fecha_cosecha_inicio=2024-06-01&fecha_cosecha_fin=2024-12-31"

# Ciclos activos en un rango de fechas
curl "http://localhost:8000/api/ciclos/?estado=EN_PROGRESO&fecha_siembra_inicio=2024-01-01&fecha_siembra_fin=2024-12-31"

# Búsqueda y ordenamiento
curl "http://localhost:8000/api/ciclos/?search=maíz&ordering=-fecha_siembra"

# Ciclos finalizados ordenados por fecha de cosecha
curl "http://localhost:8000/api/ciclos/?estado=FINALIZADO&ordering=fecha_cosecha_estimada"
```

---

## Instalación de Dependencias

Las siguientes dependencias deben estar en `requirements.txt`:

```
Django>=6.0
djangorestframework>=3.14
django-filter>=23.5
```

**Instalar:**
```bash
pip install -r requirements.txt
```

---

## Configuración

### En `settings/base.py`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'django_filters',
    'cultivos',
]

MIDDLEWARE = [
    # ...
    'cultivos.exception_handler.ErrorHandlerMiddleware',
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'cultivos.exception_handler.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

---

## Respuestas de Ejemplo

### Respuesta exitosa:
```json
{
  "id": 1,
  "nombre": "Trigo",
  "tipo": "cereal",
  "variedad": {
    "id": 1,
    "nombre": "Variedad Blanca",
    "descripcion": "Variedad de trigo blanco",
    "datos_agronomicos": {}
  },
  "unidad_productiva": "Campo Norte",
  "ciclos": [],
  "created_at": "2024-12-11T10:30:00Z",
  "updated_at": "2024-12-11T10:30:00Z"
}
```

### Respuesta de error:
```json
{
  "success": false,
  "status_code": 400,
  "error": {
    "type": "ValidationError",
    "message": "Campo nombre es requerido",
    "details": {
      "nombre": ["Este campo es obligatorio."]
    }
  }
}
```

---

## Notas Importantes

1. **Transacciones atómicas:** Todas las operaciones de creación, actualización y eliminación se ejecutan dentro de una transacción atómica. Si ocurre un error, toda la operación se revierte.

2. **Manejo de errores:** Los errores se capturan y se devuelven con un formato consistente. Nunca se expone información sensible del servidor.

3. **Filtros case-insensitive:** Los filtros de búsqueda por nombre usan `icontains` (case-insensitive) para mayor flexibilidad.

4. **Paginación:** Los resultados se paginan automáticamente (20 registros por página).

5. **Seguridad:** Se recomienda agregar autenticación y permisos según sea necesario en producción.
