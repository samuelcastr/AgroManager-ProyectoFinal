# 🚀 GUÍA DE DESPLIEGUE EN RAILWAY — Paso a Paso

**Objetivo:** Desplegar la API en producción en Railway (2-3 horas)  
**Requisito previo:** Repositorio GitHub público con el código

---

## 📋 Checklist Pre-Despliegue

- [ ] Repositorio GitHub público
- [ ] Todos los cambios pusheados a `main` o `develop`
- [ ] `.env.example` actualizado
- [ ] `requirements.txt` con todas las dependencias
- [ ] `manage.py` en la raíz del proyecto
- [ ] Dockerfile listo (opcional pero recomendado)

---

## 🔧 Paso 1: Preparar Dockerfile

Crea un archivo `Dockerfile` en la raíz del proyecto:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio de logs
RUN mkdir -p logs

# Exponer puerto 8000
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "-w", "4", "--timeout", "120"]
```

---

## 🔧 Paso 2: Crear archivo `.dockerignore`

```
.git
.gitignore
*.pyc
__pycache__
db.sqlite3
.env
.venv
venv
*.egg-info
.pytest_cache
.coverage
htmlcov
.vscode
.idea
node_modules
.DS_Store
logs/*
!logs/.gitkeep
```

---

## 🔧 Paso 3: Actualizar `config/settings/prod.py`

Asegúrate de que `prod.py` tenga:

```python
import os
from .base import *

# PRODUCCIÓN: DEBUG DEBE SER FALSE
DEBUG = False

# HOSTS desde variable de entorno
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# SEGURIDAD
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if os.getenv('CORS_ALLOWED_ORIGINS') else []

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}
```

---

## 🌐 Paso 4: Ir a Railway.app

1. Abre https://railway.app
2. Inicia sesión (o crea cuenta con GitHub)
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"

---

## 📦 Paso 5: Conectar Repositorio GitHub

1. Autoriza Railway para acceder a tus repos
2. Busca y selecciona `AgroManager-ProyectoFinal`
3. Selecciona rama: `main` (o `develop`)
4. Haz clic en "Deploy"

---

## ⚙️ Paso 6: Configurar Variables de Entorno

En el dashboard de Railway, ve a la aplicación creada:

1. Haz clic en "Variables"
2. Añade las siguientes variables:

```
DEBUG=False
SECRET_KEY=tu-clave-muy-segura-cambiar-en-produccion-xyz123
ALLOWED_HOSTS=api-produccion-railway.app,www.api-produccion-railway.app
DJANGO_SETTINGS_MODULE=config.settings.prod
DATABASE_URL=mysql://root:HyYShkillcrQSeemhSAkPpgKtxPCbCfa@tramway.proxy.rlwy.net:56935/railway
CORS_ALLOWED_ORIGINS=https://frontend-produccion.app
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

**Opcional:**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
```

---

## 🔨 Paso 7: Configurar Build & Deploy

En Railway, ve a "Settings":

### Build Command:
```bash
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

### Start Command:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 -w 4 --timeout 120
```

### Exposed Port:
```
8000
```

---

## 🚀 Paso 8: Deploy

1. Railway detectará cambios en GitHub automáticamente
2. O haz clic en "Deploy" manualmente
3. Espera 3-5 minutos mientras se construye y despliega

**Ver logs:**
- Haz clic en "Logs" para ver el progreso
- Si hay errores, se mostrarán aquí

---

## ✅ Paso 9: Verificar Despliegue

### Obtener URL Pública:

1. En Railway, haz clic en tu aplicación
2. Ve a "Deployments"
3. Busca "Domains" (algo como `api-prod-rail.railway.app`)

### Probar Health Check:

```bash
curl https://api-prod-rail.railway.app/api/core/health/
```

Debe responder:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-12T...",
  "server": "OK",
  "database": "OK"
}
```

### Probar Swagger:

Abre en el navegador:
```
https://api-prod-rail.railway.app/api/schema/swagger/
```

### Probar Login:

```bash
curl -X POST https://api-prod-rail.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin123!@"}'
```

Debe responder con tokens JWT.

---

## 📄 Paso 10: Actualizar README

Añade a la sección "Despliegue en Producción":

```markdown
## 🌐 API en Producción

**URL:** https://api-prod-rail.railway.app

- **Health Check:** https://api-prod-rail.railway.app/api/core/health/
- **Swagger:** https://api-prod-rail.railway.app/api/schema/swagger/
- **Admin:** https://api-prod-rail.railway.app/admin/

### Estado del Servidor:

| Recurso | Endpoint | Estado |
|---------|----------|--------|
| Health Check | GET /api/core/health/ | ✅ Operativo |
| Documentación | GET /api/schema/swagger/ | ✅ Disponible |
| Admin Django | GET /admin/ | ✅ Disponible |
| Login JWT | POST /api/auth/login/ | ✅ Funcional |

```

---

## 🔒 Seguridad Post-Despliegue

1. **Cambiar SECRET_KEY** en Railway (usar generador online)
2. **Cambiar contraseña del BD admin** en Railway
3. **Verificar DEBUG=False** en producción
4. **Configurar SSL/HTTPS** (Railway lo hace automático)
5. **Usar variables de entorno** en lugar de hardcoding

---

## 🐛 Solucionar Problemas

### Error: "ModuleNotFoundError: No module named '...'"
- Asegúrate de que el módulo está en `requirements.txt`
- Ejecuta `pip install -r requirements.txt` localmente

### Error: "Database connection error"
- Verifica que `DATABASE_URL` esté configurado en Railway
- Asegúrate de que la contraseña es correcta
- Prueba la conexión localmente primero

### Error: "DEBUG debe ser False en producción"
- Cambia `DEBUG=False` en las variables de entorno de Railway
- Verifica que `config/settings/prod.py` tenga `DEBUG = False`

### Static files no se cargan
- Ejecuta `python manage.py collectstatic --noinput`
- Verifica que `STATIC_ROOT` y `STATIC_URL` estén configurados

### 502 Bad Gateway
- Revisa los logs en Railway
- Asegúrate de que el puerto 8000 está expuesto
- Verifica que Gunicorn está configurado correctamente

---

## 📊 Monitoreo

### Ver Logs:
```bash
railway logs
```

### Reiniciar la aplicación:
- En Railway Dashboard → Settings → Restart

### Ver métricas:
- Railway Dashboard → Metrics (CPU, Memoria, Network)

---

## 🎉 ¡Listo!

Tu API está ahora en producción. 

**Próximos pasos:**
1. Probar todos los endpoints en producción
2. Verificar que JWT funciona
3. Revisar logs de errores
4. Preparar exposición final

---

**Tiempo estimado:** 30-45 minutos  
**Deadline:** Viernes 12 de diciembre, 00:00
