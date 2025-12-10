# Guía Completa de Endpoints - AgroManager API

## Tabla de Contenidos
1. [Autenticación](#autenticación)
2. [Cultivos](#cultivos)
3. [Inventario](#inventario)
4. [Sensores](#sensores)
5. [Core](#core)
6. [Notas Importantes](#notas-importantes)

---

## Autenticación

### POST /api/auth/register/
**Descripción:** Registrar nuevo usuario

**Campos Requeridos:**
- `username` - 3+ caracteres, solo alfanuméricos y guiones bajos
- `email` - Formato válido (usuario@dominio.com)
- `password` - 8+ caracteres, mayúscula, minúscula, número, símbolo
- `password2` - Debe coincidir exactamente con password
- `first_name` - Solo letras, 2+ caracteres
- `last_name` - Solo letras, 2+ caracteres

**Ejemplo:**
```json
{
  "username": "juan_perez_123",
  "email": "juan.perez@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "Juan",
  "last_name": "Perez"
}
```

**Respuesta (201 Created):**
```json
{
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 5,
    "username": "juan_perez_123",
    "email": "juan.perez@example.com",
    "first_name": "Juan",
    "last_name": "Perez"
  }
}
```

---

### POST /api/auth/login/
**Descripción:** Obtener JWT tokens para autenticación

**Campos Requeridos:**
- `username` - Usuario registrado
- `password` - Contraseña del usuario

**Ejemplo:**
```json
{
  "username": "juan_perez_123",
  "password": "SecurePass123!"
}
```

**Respuesta (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Duraciones:**
- Access Token: 60 minutos
- Refresh Token: 1 día

---

## Cultivos

### POST /api/cultivos/
**Descripción:** Crear nuevo cultivo con variedad opcional

**Campos:**
- `nombre` (requerido) - Nombre descriptivo del cultivo
- `tipo` (requerido) - Tipo de cultivo
- `variedad` (opcional) - Información de la variedad
- `unidad_productiva` (opcional) - Ubicación o identificador
- `sensores` (opcional) - JSON con configuración de sensores

**Tipos Válidos:** `cereal`, `leguminosa`, `frutal`, `hortaliza`, `forraje`

#### Opción 1: CON VARIEDAD
```json
{
  "nombre": "Maiz Premium",
  "tipo": "cereal",
  "variedad": {
    "nombre": "Variedad A1",
    "descripcion": "Variedad de alto rendimiento",
    "datos_agronomicos": {
      "rendimiento": "8 ton/ha",
      "ciclo": "120 dias",
      "temperatura_optima": "25-30°C",
      "humedad_requerida": "60-80%"
    }
  }
}
```

#### Opción 2: SIN VARIEDAD
```json
{
  "nombre": "Soja Hibrida",
  "tipo": "leguminosa"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 5,
  "nombre": "Maiz Premium",
  "tipo": "cereal",
  "variedad": {
    "id": 4,
    "nombre": "Variedad A1",
    "descripcion": "Variedad de alto rendimiento",
    "datos_agronomicos": {
      "rendimiento": "8 ton/ha",
      "ciclo": "120 dias",
      "temperatura_optima": "25-30°C",
      "humedad_requerida": "60-80%"
    }
  },
  "unidad_productiva": null,
  "sensores": null,
  "ciclos": [],
  "created_at": "2025-12-10T17:14:41.347715-05:00",
  "updated_at": "2025-12-10T17:14:41.371805-05:00"
}
```

---

### GET /api/cultivos/
**Descripción:** Listar todos los cultivos

**Parámetros Query:**
- `page` - Número de página (paginación)
- `search` - Buscar por nombre
- `ordering` - Ordenar por campo

**Ejemplo:**
```
GET /api/cultivos/?search=maiz&page=1
```

**Respuesta (200 OK):**
```json
{
  "count": 9,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 9,
      "nombre": "Arroz Integral Premium",
      "tipo": "cereal",
      "variedad": {
        "id": 4,
        "nombre": "Arroz Dorado",
        "descripcion": "Arroz de grano largo de alto rendimiento",
        "datos_agronomicos": {
          "rendimiento": "6 ton/ha",
          "ciclo": "135 dias"
        }
      },
      "unidad_productiva": null,
      "sensores": null,
      "ciclos": [],
      "created_at": "2025-12-10T17:14:41.347715-05:00",
      "updated_at": "2025-12-10T17:14:41.371805-05:00"
    }
  ]
}
```

---

### GET /api/cultivos/tipos/
**Descripción:** Obtener tipos de cultivos disponibles

**Respuesta (200 OK):**
```json
{
  "tipos": [
    "cereal",
    "leguminosa",
    "frutal",
    "hortaliza",
    "forraje"
  ]
}
```

---

## Inventario

### POST /api/inventario/insumos/
**Descripción:** Crear nuevo insumo

**Campos Requeridos:**
- `nombre` - Nombre único del insumo, 2+ caracteres
- `unidad_medida` - Unidad de medida (kg, litros, unidades, gramos, toneladas)
- `stock_minimo` - Número positivo
- `precio_unitario` - Número positivo (decimal)

**Campos Opcionales:**
- `proveedor` - Nombre del proveedor

**Ejemplo:**
```json
{
  "nombre": "Fertilizante NPK 10-10-10",
  "unidad_medida": "kg",
  "stock_minimo": 50,
  "precio_unitario": 1500.00,
  "proveedor": "Agro Distribuidora"
}
```

**Unidades Comunes:** `kg`, `litros`, `unidades`, `gramos`, `toneladas`

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "nombre": "Fertilizante NPK 10-10-10",
  "unidad_medida": "kg",
  "stock_minimo": 50,
  "precio_unitario": "1500.00",
  "proveedor": "Agro Distribuidora"
}
```

---

### POST /api/inventario/lotes/
**Descripción:** Crear nuevo lote de insumo

**Campos Requeridos:**
- `insumo` - ID del insumo existente
- `cantidad` - Número positivo
- `fecha_ingreso` - Formato YYYY-MM-DD
- `fecha_vencimiento` - Debe ser mayor a fecha_ingreso

**Campos Opcionales:**
- `lote_proveedor` - Código del lote del proveedor

**Ejemplo:**
```json
{
  "insumo": 1,
  "cantidad": 100,
  "fecha_ingreso": "2025-12-10",
  "fecha_vencimiento": "2026-12-10",
  "lote_proveedor": "LOTE-001"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "insumo": 1,
  "cantidad": 100,
  "fecha_ingreso": "2025-12-10",
  "fecha_vencimiento": "2026-12-10",
  "lote_proveedor": "LOTE-001"
}
```

---

### POST /api/inventario/movimientos/
**Descripción:** Registrar movimiento de stock (entrada o salida)

**Campos Requeridos:**
- `lote` - ID del lote existente
- `tipo` - ENTRADA o SALIDA
- `cantidad` - Número positivo
- `motivo` - Razón del movimiento

**Tipos Válidos:** `ENTRADA`, `SALIDA`

**Ejemplo:**
```json
{
  "lote": 1,
  "tipo": "ENTRADA",
  "cantidad": 50,
  "motivo": "Compra a proveedor"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "lote": 1,
  "tipo": "ENTRADA",
  "cantidad": 50,
  "motivo": "Compra a proveedor",
  "fecha": "2025-12-10T17:30:00Z"
}
```

---

### GET /api/inventario/movimientos/
**Descripción:** Listar todos los movimientos de stock

**Respuesta (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "lote": 1,
      "tipo": "ENTRADA",
      "cantidad": 50,
      "motivo": "Compra a proveedor",
      "fecha": "2025-12-10T17:30:00Z"
    }
  ]
}
```

---

### POST /api/inventario/ajuste-masivo/
**Descripción:** Realizar ajuste masivo de inventario

**Campos Requeridos:**
- `items` - Array de objetos con lote y cantidad_nueva
- `motivo` - Razón del ajuste

**Ejemplo:**
```json
{
  "items": [
    {"lote": 1, "cantidad_nueva": 150},
    {"lote": 2, "cantidad_nueva": 200}
  ],
  "motivo": "Inventario fisico"
}
```

**Respuesta (201 Created):**
```json
{
  "mensaje": "Ajuste masivo realizado exitosamente",
  "items_ajustados": 2,
  "motivo": "Inventario fisico"
}
```

---

### GET /api/inventario/alertas-stock/
**Descripción:** Obtener insumos con stock bajo (por debajo del mínimo)

**Respuesta (200 OK):**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "nombre": "Fertilizante NPK 10-10-10",
      "unidad_medida": "kg",
      "stock_minimo": 50,
      "stock_actual": 30,
      "diferencia": -20
    }
  ]
}
```

---

## Sensores

### POST /api/sensores/
**Descripción:** Crear nuevo sensor IoT

**Campos Requeridos:**
- `serial` - Número de serie único, 2+ caracteres
- `tipo` - Tipo de sensor (HUMEDAD, PH, TEMPERATURA)
- `ubicacion` - Descripción de ubicación física

**Campos Opcionales:**
- `unidad_productiva` - ID de la unidad productiva

**Tipos Válidos:** `HUMEDAD`, `PH`, `TEMPERATURA`

**Ejemplo:**
```json
{
  "serial": "SENSOR-001",
  "tipo": "HUMEDAD",
  "ubicacion": "Campo A, Fila 5",
  "unidad_productiva": 1
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "serial": "SENSOR-001",
  "tipo": "HUMEDAD",
  "ubicacion": "Campo A, Fila 5",
  "unidad_productiva": 1,
  "creado": "2025-12-10T17:30:00Z"
}
```

---

### GET /api/sensores/
**Descripción:** Listar todos los sensores

**Respuesta (200 OK):**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "serial": "SENSOR-001",
      "tipo": "HUMEDAD",
      "ubicacion": "Campo A, Fila 5",
      "unidad_productiva": 1,
      "creado": "2025-12-10T17:30:00Z"
    }
  ]
}
```

---

### POST /api/sensores/lecturas/
**Descripción:** Registrar nueva lectura de sensor

**Campos Requeridos:**
- `sensor` - ID del sensor existente
- `valor` - Número decimal (valor leído)
- `timestamp` - Formato ISO 8601
- `es_valida` - Boolean (true/false)

**Ejemplo:**
```json
{
  "sensor": 1,
  "valor": 65.5,
  "timestamp": "2025-12-10T15:30:00Z",
  "es_valida": true
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "sensor": 1,
  "valor": 65.5,
  "timestamp": "2025-12-10T15:30:00Z",
  "es_valida": true
}
```

---

### GET /api/sensores/lecturas/
**Descripción:** Listar todas las lecturas de sensores

**Parámetros Query:**
- `sensor` - Filtrar por ID de sensor
- `page` - Número de página

**Respuesta (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "sensor": 1,
      "valor": 65.5,
      "timestamp": "2025-12-10T15:30:00Z",
      "es_valida": true
    }
  ]
}
```

---

### GET /api/sensores/tipos/
**Descripción:** Obtener tipos de sensores disponibles

**Respuesta (200 OK):**
```json
{
  "tipos": [
    "HUMEDAD",
    "PH",
    "TEMPERATURA"
  ]
}
```

---

## Core

### GET /api/core/health/
**Descripción:** Verificar estado del sistema

**Respuesta (200 OK):**
```json
{
  "server": "OK",
  "database": "OK"
}
```

---

### GET /api/core/profiles/
**Descripción:** Listar perfiles de usuario (requiere autenticación)

**Respuesta (200 OK):**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "username": "juan_perez_123",
        "email": "juan.perez@example.com"
      },
      "phone": "1234567890",
      "role": "agricultor",
      "document": "12345678",
      "is_verified": true,
      "created_at": "2025-12-10T17:30:00Z"
    }
  ]
}
```

---

## Notas Importantes

### 1. Autenticación JWT
- **Todos los endpoints** (excepto `/auth/register/` y `/auth/login/`) requieren JWT token
- Incluir header en todas las solicitudes:
  ```
  Authorization: Bearer <access_token>
  ```

### 2. Formatos de Fecha y Hora
- **Fechas:** `YYYY-MM-DD` (ej: 2025-12-10)
- **Timestamps:** ISO 8601 (ej: 2025-12-10T15:30:00Z)

### 3. Campos JSON (datos_agronomicos, sensores)
- Deben ser diccionarios válidos
- Pueden contener cualquier estructura de datos
- Válidos: `{}`, `null`, `{"key": "value"}`

### 4. IDs y Referencias
- Todos los IDs que referencian otros objetos deben existir
- El servidor retornará 400 Bad Request si un ID no existe

### 5. Códigos de Respuesta HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Solicitud exitosa (GET, actualización sin cambios) |
| 201 | Created | Recurso creado exitosamente (POST) |
| 400 | Bad Request | Datos inválidos en la solicitud |
| 401 | Unauthorized | Requiere autenticación JWT |
| 403 | Forbidden | Acceso denegado (permisos insuficientes) |
| 404 | Not Found | Recurso no existe |
| 409 | Conflict | Conflicto (ej: email ya registrado) |
| 500 | Server Error | Error interno del servidor |

### 6. Validaciones Comunes

**Username:**
- Mínimo 3 caracteres
- Solo alfanuméricos y guiones bajos
- Debe ser único

**Email:**
- Formato válido
- Debe ser único
- No puede contener caracteres especiales como `;`

**Contraseña:**
- Mínimo 8 caracteres
- Al menos una mayúscula
- Al menos una minúscula
- Al menos un número
- Al menos un símbolo especial

**Nombres (first_name, last_name):**
- Solo letras
- Mínimo 2 caracteres

### 7. Paginación
- El servidor retorna resultados paginados por defecto
- Incluyen: `count` (total), `next` (próxima página), `previous` (página anterior), `results` (datos)
- Parámetro: `?page=1`

### 8. Búsqueda y Filtrado
- Parámetro: `?search=término`
- Parámetro: `?ordering=campo` (ordenamiento)

### 9. Errores Comunes

```json
{
  "detail": "Error en la solicitud",
  "code": 400,
  "errors": {
    "campo": ["Mensaje de error específico"]
  }
}
```

---

## Ejemplos Completos

### Flujo Completo: Registro → Login → Crear Cultivo

#### 1. Registrar usuario
```bash
POST http://localhost:8000/api/auth/register/
Content-Type: application/json

{
  "username": "juan_perez_123",
  "email": "juan.perez@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "Juan",
  "last_name": "Perez"
}
```

#### 2. Login (obtener tokens)
```bash
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
  "username": "juan_perez_123",
  "password": "SecurePass123!"
}
```

Respuesta:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 3. Crear cultivo (con token)
```bash
POST http://localhost:8000/api/cultivos/
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "nombre": "Maiz Premium",
  "tipo": "cereal",
  "variedad": {
    "nombre": "Variedad A1",
    "descripcion": "Alto rendimiento",
    "datos_agronomicos": {
      "rendimiento": "8 ton/ha",
      "ciclo": "120 dias"
    }
  }
}
```

---

## Soporte

Para más información o reportar problemas, contacta al equipo de desarrollo.

**Última actualización:** 10 de Diciembre de 2025
