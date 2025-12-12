# 🚀 GUÍA DE DESPLIEGUE EN RENDER — Paso a Paso (Con Railway para BD)

**Objetivo:** Desplegar la API en Render.com (Frontend + Backend)  
**Base de datos:** Railway MySQL (ya configurada)  
**Tiempo estimado:** 45 minutos

---

## 📋 Requisitos Previos

- [ ] Repositorio GitHub público
- [ ] Código pusheado a rama `main` o `develop`
- [ ] `Procfile` en la raíz del proyecto ✅ (Ya existe)
- [ ] `requirements.txt` actualizado ✅ (Ya existe)
- [ ] Cuenta en Render.com (https://render.com)
- [ ] BD en Railway funcionando ✅ (Ya configurada)

---

## 🔧 Paso 1: Ir a Render.com

1. Abre https://render.com
2. Inicia sesión con GitHub (recomendado)
3. Haz clic en "New +" → "Web Service"

---

## 🔧 Paso 2: Conectar Repositorio GitHub

1. Selecciona "Deploy from a Git repository"
2. Autoriza Render para acceder a GitHub
3. Busca y selecciona: `AgroManager-ProyectoFinal`
4. Selecciona rama: `main` (o `develop`)
5. Haz clic en "Connect"

---

## ⚙️ Paso 3: Configurar Servicio Web

### Configuración Básica:

| Campo | Valor |
|-------|-------|
| Name | `agromanager-api` |
| Environment | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT -w 4` |
| Plan | Free (o Starter si necesitas más recursos) |

### Configuración Avanzada:

- **Auto-deploy:** Habilitado (desde main branch)
- **Root Directory:** (dejar vacío)
- **Runtime:** Python 3.11

---

## 🔐 Paso 4: Agregar Variables de Entorno

En Render, ve a "Environment":

### Variables Críticas:

```
DJANGO_SETTINGS_MODULE=config.settings.prod
DEBUG=False
SECRET_KEY=TU-CLAVE-SUPER-SEGURA-AQUI-CAMBIAR-PERIODICAMENTE-XYZ123!@#
ALLOWED_HOSTS=agromanager-api.onrender.com,www.agromanager-api.onrender.com,localhost
DATABASE_URL=mysql://root:HyYShkillcrQSeemhSAkPpgKtxPCbCfa@tramway.proxy.rlwy.net:56935/railway
```

### Variables Recomendadas (Producción):

```
CSRF_TRUSTED_ORIGINS=https://agromanager-api.onrender.com
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### Variables Opcionales (Email):

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@tudominio.com
EMAIL_HOST_PASSWORD=tu-app-password
```

---

## 🎯 Paso 5: Configurar Procfile

El `Procfile` ya está en la raíz del proyecto:

```procfile
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT -w 4 --timeout 120
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

**Esto asegura que:**
- ✅ Las migraciones se ejecuten automáticamente
- ✅ Los static files se recopilen
- ✅ La app inicie con Gunicorn correctamente

---

## 🚀 Paso 6: Deploy

1. En Render, haz clic en "Create Web Service"
2. Render comenzará el build automáticamente
3. Espera 3-5 minutos mientras se construye y despliega
4. Verás los logs en la sección "Logs"

### Monitorear el despliegue:

```
📊 Build phase:
   ✅ pip install -r requirements.txt
   ✅ Dependencias instaladas

🔧 Release phase:
   ✅ python manage.py migrate
   ✅ python manage.py collectstatic

🚀 Web service starting:
   ✅ gunicorn iniciado en puerto 10000
   ✅ Escuchando conexiones
```

---

## ✅ Paso 7: Verificar Despliegue

### Obtener URL Pública:

En Render Dashboard → Tu servicio → "Domains"

Ejemplo: `https://agromanager-api.onrender.com`

### Test 1: Health Check

```bash
curl https://agromanager-api.onrender.com/api/core/health/
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-12T...",
  "server": "OK",
  "database": "OK"
}
```

### Test 2: Swagger Docs

Abre en navegador:
```
https://agromanager-api.onrender.com/api/schema/swagger/
```

### Test 3: Admin Django

```
https://agromanager-api.onrender.com/admin/
Usuario: admin
Contraseña: Admin123!@
```

### Test 4: Login JWT

```bash
curl -X POST https://agromanager-api.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin123!@"
  }'
```

Respuesta esperada:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Test 5: Registro con Rol

```bash
curl -X POST https://agromanager-api.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "agricultor_test",
    "email": "agricultor@example.com",
    "password": "Secure123!@#",
    "password2": "Secure123!@#",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "agricultor",
    "phone": "+57 310 123 4567"
  }'
```

---

## 📊 Paso 8: Monitoreo Continuo

### Ver Logs:

En Render Dashboard → "Logs" o:

```bash
# Si usas Render CLI
render logs <service-id>
```

### Reiniciar la app:

Render Dashboard → "Suspend" → "Resume"

### Métricas:

Render Dashboard → "Metrics" (CPU, Memoria, Network)

---

## 🔒 Paso 9: Seguridad en Producción

### ✅ Cambiar Credenciales

1. **SECRET_KEY:** Generar nueva con https://djecrety.ir/
   - Copiar y pegar en Render variables de entorno
   - Reiniciar servicio

2. **admin password:** Cambiar password del usuario admin

   ```bash
   # En Render Shell (Premium) o localmente:
   python manage.py shell --settings=config.settings.prod
   from django.contrib.auth.models import User
   u = User.objects.get(username='admin')
   u.set_password('NuevaPasswordSegura123!@#')
   u.save()
   ```

3. **DATABASE_URL:** Ya segura en Render (variables privadas)

### ✅ Configurar HTTPS

- Render proporciona HTTPS automático (certificado Let's Encrypt)
- HSTS activado (3 años)
- Redirección forzada a HTTPS

### ✅ Backup de BD

- En Railway: Configurar backups automáticos
- Guardar contraseñas en lugar seguro (1Password, Bitwarden, etc.)

---

## 🐛 Solucionar Problemas

### Error: "No module named 'MySQLdb'"

**Causa:** mysqlclient no está instalado  
**Solución:** Agregar a requirements.txt:

```
mysqlclient==2.2.7
```

### Error: "Database connection error"

**Causa:** DATABASE_URL incorrea o BD no accesible  
**Solución:**
1. Verificar que Railway DB está funcionando
2. Probar conexión localmente primero
3. Revisar credenciales en Render variables

### Error: "DEBUG debe ser False en producción"

**Causa:** DEBUG=True en las variables  
**Solución:** Cambiar `DEBUG=False` en Render

### Error: "502 Bad Gateway"

**Causa:** Gunicorn crash o timeout  
**Solución:**
1. Revisar logs
2. Aumentar timeout: `--timeout 120`
3. Aumentar workers: `-w 8`

### Error: "Static files not found"

**Causa:** collectstatic no se ejecutó  
**Solución:**
1. Verificar que el Procfile tiene el release command
2. Ejecutar manualmente: `python manage.py collectstatic --noinput`

---

## 📝 Paso 10: Actualizar README

Agrega a tu README.md:

```markdown
## 🌐 API en Producción (Render)

**URL:** https://agromanager-api.onrender.com

### Endpoints Disponibles:

| Recurso | Endpoint | Status |
|---------|----------|--------|
| Health Check | `GET /api/core/health/` | ✅ |
| Swagger Docs | `GET /api/schema/swagger/` | ✅ |
| Admin Panel | `GET /admin/` | ✅ |
| Login | `POST /api/auth/login/` | ✅ |
| Register | `POST /api/auth/register/` | ✅ |
| Cultivos CRUD | `GET/POST /api/cultivos/` | ✅ |
| Inventario CRUD | `GET/POST /api/inventario/insumos/` | ✅ |
| Sensores CRUD | `GET/POST /api/sensores/` | ✅ |

### Autenticación:

Todos los endpoints (excepto `/health/`, `/login/`, `/register/`) requieren JWT Bearer Token:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://agromanager-api.onrender.com/api/cultivos/
```

### Database:

- Tipo: MySQL (Railway)
- Host: tramway.proxy.rlwy.net:56935
- Status: ✅ Conectada
```

---

## ✨ ¡Listo!

Tu API está ahora en producción en Render:

```
🎉 Base de datos: Railway MySQL
🎉 Backend: Render.com  
🎉 HTTPS: Automático
🎉 Logs: En tiempo real
🎉 Auto-deploy: Desde GitHub
```

---

## 🚦 Siguientes Pasos

1. Probar todos los endpoints en producción
2. Verificar que JWT funciona
3. Revisar logs de errores
4. Preparar exposición final (10 minutos)
5. Presentar proyecto 🎊

---

**Tiempo total:** 45 minutos  
**Deadline:** Viernes 12 de diciembre, 00:00  
**Status:** ✅ LISTO PARA PRODUCCIÓN
