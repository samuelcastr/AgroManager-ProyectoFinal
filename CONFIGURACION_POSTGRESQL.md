# Configuración de PostgreSQL para AgroManager

## Requisitos Previos

1. **PostgreSQL instalado** - Descarga desde https://www.postgresql.org/download/
2. **DBeaver (opcional)** - Cliente GUI para visualizar la BD

---

## Paso 1: Instalar PostgreSQL

### Windows
1. Descarga el instalador desde https://www.postgresql.org/download/windows/
2. Ejecuta el instalador
3. En la instalación, establece:
   - **Usuario:** `postgres`
   - **Contraseña:** `postgres` (o la que prefieras)
   - **Puerto:** `5432` (por defecto)
4. Marca "PostgreSQL Server" durante la instalación
5. Marca "pgAdmin 4" (gestor GUI)

### Verificar instalación
```bash
# En PowerShell
psql --version
```

---

## Paso 2: Instalar dependencias Python

Si no las tienes instaladas:

```bash
# En la raíz del proyecto
pip install -r requirements.txt

# O específicamente:
pip install psycopg2-binary==2.9.9
```

---

## Paso 3: Crear la Base de Datos

### Opción A: Usar psql (terminal)

```bash
# Conéctate a PostgreSQL
psql -U postgres

# En la terminal psql, ejecuta:
CREATE DATABASE agromanager OWNER postgres;
CREATE USER agromanager_user WITH PASSWORD 'agromanager_pass';
ALTER ROLE agromanager_user SET client_encoding TO 'utf8';
ALTER ROLE agromanager_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE agromanager_user SET default_transaction_deferrable TO on;
ALTER ROLE agromanager_user SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE agromanager_db TO agromanager_user;
\q
```

### Opción B: Usar pgAdmin 4 (GUI)

1. Abre pgAdmin 4
2. Conéctate con usuario `postgres` y contraseña `postgres`
3. Click derecho en "Databases" → "Create" → "Database"
4. Nombre: `agromanager_db`
5. Owner: `postgres`
6. Crear

---

## Paso 4: Configurar credenciales en Django

### Opción A: Editar config/settings/dev.py (ya está hecho)

El archivo ya está actualizado con:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'agromanager_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Opción B: Usar variables de entorno (recomendado)

1. Crea archivo `.env` en la raíz del proyecto:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=agromanager_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

2. Modifica `config/settings/dev.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

---

## Paso 5: Aplicar Migraciones

```bash
# En la raíz del proyecto
python manage.py migrate --settings=config.settings.dev
```

Deberías ver salida similar a:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, cultivos, inventario, sensores, sessions
Running migrations:
  Applying admin.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

## Paso 6: Verificar Conexión

```bash
# Prueba la conexión
python manage.py dbshell --settings=config.settings.dev

# En la terminal PostgreSQL que se abre:
SELECT 1;
\q
```

---

## Paso 7: Instalar DBeaver (Opcional pero Recomendado)

### Descargar DBeaver
- URL: https://dbeaver.io/download/
- Descarga la versión "Community Edition" para Windows

### Conectarse a PostgreSQL desde DBeaver

1. Abre DBeaver
2. Clic en "New Database Connection"
3. Selecciona "PostgreSQL"
4. Configura:
   - **Host:** localhost
   - **Port:** 5432
   - **Database:** agromanager_db
   - **Username:** postgres
   - **Password:** postgres
5. Clic en "Test Connection"
6. Clic en "Finish"

---

## Paso 8: Iniciar el Servidor

```bash
# Con PostgreSQL ejecutándose
python manage.py runserver --settings=config.settings.dev
```

Deberías ver:
```
Starting development server at http://127.0.0.1:8000/
```

---

## Verificar en Swagger

1. Accede a: http://localhost:8000/swagger/
2. Prueba endpoints (requieren JWT)
3. Verifica que los datos se guardan

---

## Comandos Útiles PostgreSQL

### Ver todas las bases de datos
```bash
psql -U postgres -c "\l"
```

### Conectarse a una BD específica
```bash
psql -U postgres -d agromanager_db
```

### Ver todas las tablas
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```

### Ejecutar dump de la BD (backup)
```bash
pg_dump -U postgres -d agromanager_db > backup.sql
```

### Restaurar dump
```bash
psql -U postgres -d agromanager_db < backup.sql
```

---

## Troubleshooting

### Error: "could not connect to server"
- Verifica que PostgreSQL esté ejecutándose
- En Windows, abre "Services" y busca "PostgreSQL"
- Reinicia el servicio si es necesario

### Error: "FATAL: Ident authentication failed"
- Edita `pg_hba.conf` (en la carpeta de PostgreSQL)
- Cambia `ident` a `md5` o `scram-sha-256` en la línea de localhost
- Reinicia PostgreSQL

### Error: "password authentication failed"
- Verifica usuario y contraseña en settings/dev.py
- Asegúrate de que el usuario tiene permisos en la BD
- Usa psql para resetear contraseña:
  ```sql
  ALTER ROLE postgres WITH PASSWORD 'new_password';
  ```

### La BD se creó pero no tiene tablas
- Ejecuta migraciones: `python manage.py migrate --settings=config.settings.dev`

---

## Estructura de Tablas en DBeaver

Después de migraciones, verás estas tablas:

```
agromanager_db
├── admin_log (auditoría de cambios)
├── auth_group
├── auth_group_permissions
├── auth_permission
├── auth_user
├── auth_user_groups
├── auth_user_user_permissions
├── core_userprofile
├── core_unidadproductiva
├── core_auditlog
├── core_passwordresettoken
├── cultivos_variedad
├── cultivos_cultivo
├── cultivos_ciclosiembra
├── inventario_insumo
├── inventario_lote
├── inventario_movimientostock
├── inventario_ajuste
├── sensores_sensor
├── sensores_lectura
└── sessions
```

---

## Notas Importantes

1. **Usuario PostgreSQL predeterminado:** `postgres` con contraseña `postgres`
2. **Puerto por defecto:** `5432`
3. **Archivo de configuración:** `config/settings/dev.py`
4. **BD por defecto para desarrollo:** `agromanager_db`

---

## Próximos Pasos

1. ✅ Instalar PostgreSQL
2. ✅ Crear base de datos
3. ✅ Aplicar migraciones
4. ✅ Instalar DBeaver (opcional)
5. ✅ Conectar DBeaver a PostgreSQL
6. ✅ Ver datos en DBeaver
7. ✅ Probar API

---

**Última actualización:** 10 de Diciembre de 2025
