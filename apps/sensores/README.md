# App Sensores – AgroManager

Esta app gestiona sensores IoT y sus lecturas dentro del sistema AgroManager.

## ¿Qué hace?
- Permite registrar sensores agrícolas (tipo, ubicación, serial).
- Almacena lecturas de sensores (valor, timestamp, datos crudos).
- Expone endpoints para consultar sensores y lecturas.
- Permite ingesta masiva de lecturas vía API.
- Soporta filtros por fecha, tipo y valores.

## Endpoints principales
- `/api/sensores/` — CRUD de sensores
- `/api/lecturas/` — Listar y crear lecturas individuales
- `/api/lecturas/bulk/` — Ingesta masiva de lecturas (POST)
- `/api/sensores/{id}/ultimas/` — Últimas lecturas de un sensor

## Ejemplo de uso
1. Registrar un sensor:
   ```json
   {
     "serial": "SENSOR-001",
     "tipo": "HUMEDAD",
     "ubicacion": "Parcela Norte"
   }
   ```
2. Ingresar lecturas:
   ```json
   [
     {"sensor": 1, "timestamp": "2025-12-09T10:00:00Z", "valor": 23.5},
     {"sensor": 1, "timestamp": "2025-12-09T11:00:00Z", "valor": 22.8}
   ]
   ```

## Pruebas
Ejecuta los tests de la app:
```powershell
python manage.py test sensores
```

## Autor
Cielos Alexandra Rodríguez

