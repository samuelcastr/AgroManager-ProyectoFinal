# 🚀 INSTRUCCIONES PASO A PASO: DESPLIEGUE EN RENDER

**Tiempo estimado:** 45 minutos  
**Dificultad:** Media (sin conocimiento previo de Render)  
**Resultado:** API en producción en https://agromanager-api.onrender.com

---

## ✅ VERIFICACIONES PREVIAS (5 minutos)

Antes de desplegar, asegúrate que TODO esté listo localmente:

```bash
# 1. Verificar que estás en la rama correcta
git status
# Debe decir: On branch prueva-antes-main

# 2. Verificar último commit
git log -1 --oneline
# Debe mostrar: documentos finales

# 3. Verificar que no hay cambios sin commitear
git status
# Debe decir: nothing to commit, working tree clean

# 4. Verificar Procfile existe
ls -la Procfile
# Debe existir y tener 2 líneas (web + release)

# 5. Verificar requirements.txt actualizado
cat requirements.txt | grep -E "gunicorn|Django|rest_framework"
# Debe mostrar estas librerías
```

**Si algo falla:** Revisa [CHECKLIST_FINAL.md](CHECKLIST_FINAL.md) sección "COSAS QUE NO OLVIDES"

---

## 🔐 PREPARAR VARIABLES DE ENTORNO (5 minutos)

### Necesitas tener listos:

#### 1. SECRET_KEY (Nueva para producción)

```bash
# Opción A: Generar una nueva en Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Ejemplo de salida:
# 'ab12cd34ef56gh78ij90kl12mn34op56qr78st90uv12wx34yz'

# Guarda este valor para el paso de Render
```

#### 2. DATABASE_URL (Ya tienes en .env)

```bash
# Ver tu DATABASE_URL actual
cat .env | grep DATABASE_URL

# Debería verse así:
# DATABASE_URL=mysql://root:HyYShkillcrQSeemhSAkPpgKtxPCbCfa@tramway.proxy.rlwy.net:56935/railway
```

#### 3. ALLOWED_HOSTS

```
agromanager-api.onrender.com,localhost,127.0.0.1
```

#### 4. CORS_ALLOWED_ORIGINS

```
https://agromanager-api.onrender.com
```

---

## 🌐 CREAR WEB SERVICE EN RENDER (15 minutos)

### PASO 1: Ir a Render.com

```
1. Abre: https://render.com
2. Si no tienes cuenta, haz clic en "Sign up"
3. Puedes registrarte con GitHub (recomendado)
```

### PASO 2: Conectar GitHub

```
1. En el dashboard de Render, haz clic en "New +"
2. Selecciona "Web Service"
3. Haz clic en "Connect Repository"
4. Busca: AgroManager-ProyectoFinal
5. Haz clic en "Connect"
6. Render te llevará a configurar el servicio
```

### PASO 3: Configurar Web Service

Completa los campos como sigue:

```
Name:                    agromanager-api
Root Directory:          (dejar vacío)
Environment:             Python 3
Region:                  North America (Oregon)
Branch:                  prueva-antes-main
Build Command:           pip install -r requirements.txt
Start Command:           gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

**IMPORTANTE:** El Start Command se toma del Procfile automáticamente, así que déjalo como arriba.

### PASO 4: Agregar Variables de Entorno

En la misma pantalla, busca "Environment" y haz clic en "Add Environment Variable"

Agrega estas variables (una por una):

| Key | Value | Notas |
|-----|-------|-------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.prod` | Obligatorio |
| `DEBUG` | `False` | NUNCA True en producción |
| `SECRET_KEY` | `(tu SECRET_KEY generada)` | La que generaste con el comando |
| `DATABASE_URL` | `mysql://root:HyYShkillcrQSeemhSAkPpgKtxPCbCfa@tramway.proxy.rlwy.net:56935/railway` | De Railway |
| `ALLOWED_HOSTS` | `agromanager-api.onrender.com,localhost,127.0.0.1` | Debe incluir dominio de Render |
| `CORS_ALLOWED_ORIGINS` | `https://agromanager-api.onrender.com` | Para JavaScript desde frontend |

**Dónde agregar:**

```
En Render dashboard:
↓
Tu Web Service (agromanager-api)
↓
Settings (arriba a la derecha)
↓
Environment (en el menú izquierdo)
↓
Add Environment Variable (botón azul)
```

### PASO 5: Configurar Build & Deploy

En Settings, busca:

```
Build Command:          pip install -r requirements.txt
Start Command:          gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Si está vacío, cópialo de arriba.

**Plan:** Render Free es ok para demostración. Si quieres producción real, elige Starter ($7/mes).

---

## 🚀 EJECUTAR DESPLIEGUE (10 minutos)

### PASO 6: Deploy

```
1. Haz clic en "Create Web Service" (botón azul al fondo)
2. Render automáticamente inicia el build
3. Verás un log en tiempo real (ESTÁ BIEN si toma 3-5 minutos)
4. Espera a que diga "Build successful" (en verde)
```

**Qué esperar en los logs:**

```
✅ Installing Python packages...
✅ Running migrations...
✅ Collecting static files...
✅ Starting gunicorn...
✅ Server started on port 10000
```

**Si ves errores:**
- `ModuleNotFoundError: No module named 'rest_framework'` → Faltan dependencias en requirements.txt
- `Cannot connect to database` → DATABASE_URL incorrecto
- `Secret key not found` → Olvidaste agregar SECRET_KEY variable

Ver sección "Troubleshooting" más abajo.

### PASO 7: Obtener URL Pública

```
En el dashboard de Render:
1. Tu Web Service mostrará algo como:
   agromanager-api.onrender.com
   
2. Este es tu URL pública en PRODUCCIÓN

3. Cópiala, la necesitarás para testing
```

---

## ✅ VERIFICACIONES POST-DESPLIEGUE (10 minutos)

Después de que el deploy termine, verifica que TODO funciona:

### Verificación 1: Health Check

```bash
curl https://agromanager-api.onrender.com/api/core/health/

# Respuesta esperada (200 OK):
{
  "status": "healthy",
  "database": "connected",
  "django": "operational"
}
```

### Verificación 2: Swagger Funciona

```
Abre en navegador:
https://agromanager-api.onrender.com/api/schema/swagger/

Debería verse:
- Swagger UI funcional
- Todos los endpoints listados
- Opción de "Try it out"
```

### Verificación 3: Registro de Usuario

```bash
curl -X POST https://agromanager-api.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "TestPassword123!@#",
    "password2": "TestPassword123!@#",
    "first_name": "Test",
    "last_name": "User",
    "role": "agricultor",
    "phone": "+57 310 123 4567"
  }'

# Respuesta esperada (201 Created):
{
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 1,
    "username": "test_user",
    "email": "test@example.com",
    "role": "agricultor"
  }
}
```

### Verificación 4: Login y JWT

```bash
curl -X POST https://agromanager-api.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "TestPassword123!@#"
  }'

# Respuesta esperada (200 OK):
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Verificación 5: Usar Token para Acceso

```bash
# Guarda el token de acceso de la respuesta anterior
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Intenta listar cultivos (con autenticación)
curl https://agromanager-api.onrender.com/api/cultivos/ \
  -H "Authorization: Bearer $TOKEN"

# Respuesta esperada (200 OK):
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

**Si todas las verificaciones pasan ✅, ¡TU DESPLIEGUE ES EXITOSO!**

---

## 🔧 TROUBLESHOOTING

### Error: "Cannot connect to database"

```
Síntoma: Error en logs de Render sobre database connection

Solución:
1. Verifica que DATABASE_URL esté exacto en Render Environment
2. Copia-pega desde tu .env local:
   mysql://root:HyYShkillcrQSeemhSAkPpgKtxPCbCfa@tramway.proxy.rlwy.net:56935/railway
3. En Render, haz clic en "Manual Deploy" para reintentar
```

### Error: "ModuleNotFoundError: No module named 'rest_framework'"

```
Síntoma: Build falla porque faltan dependencias

Solución:
1. Verifica que requirements.txt tenga:
   Django==4.2.8
   djangorestframework==3.14.0
   mysqlclient==2.2.0
   gunicorn==21.2.0
   python-dotenv==1.0.0
   dj-database-url==2.1.0
   (etc.)
2. Haz git add + git commit + git push
3. En Render, "Manual Deploy"
```

### Error: "ALLOWED_HOSTS error"

```
Síntoma: Error 400 "Invalid Host Header"

Solución:
1. En Render Settings → Environment
2. Verifica que ALLOWED_HOSTS incluya:
   agromanager-api.onrender.com,localhost,127.0.0.1
3. Guarda cambios
4. "Manual Deploy" en Render
```

### Error: "SECRET_KEY not found"

```
Síntoma: Error sobre SECRET_KEY en logs

Solución:
1. Genera nueva con:
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
2. En Render Settings → Environment
3. Agrega: SECRET_KEY = (tu valor generado)
4. "Manual Deploy"
```

### Error: "static files not found"

```
Síntoma: CSS/JS no carga en admin

Solución:
1. En Procfile, asegúrate que release command incluye:
   release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
2. Está bien si ya está, Render lo ejecuta automáticamente
3. No necesitas hacer nada, solo esperar a que collectstatic termine
```

---

## 📝 ACTUALIZAR DOCUMENTACIÓN

Después de que despliegue sea exitoso:

### Actualizar README.md

```markdown
## 🚀 Despliegue en Producción

La API está desplegada en Render:

**URL Base de Producción:** https://agromanager-api.onrender.com

### Acceso

- **Swagger UI:** https://agromanager-api.onrender.com/api/schema/swagger/
- **Admin Django:** https://agromanager-api.onrender.com/admin/
- **Health Check:** https://agromanager-api.onrender.com/api/core/health/

### Para Desarrolladores

Base de datos en Railway MySQL:
- Host: tramway.proxy.rlwy.net:56935
- Base de datos: railway
- Usuario: root

Para cambiar variables de entorno:
1. Ir a Render dashboard
2. Tu Web Service (agromanager-api)
3. Settings → Environment
4. Editar variables
5. Auto-deploy sucede después de guardar
```

### Agregar al README.md

```bash
cd c:\Users\samue\Documents\AgroManager-ProyectoFinal

# Editar README.md con tu editor favorito
# Agregar sección arriba sobre "Despliegue en Producción"

git add README.md
git commit -m "README: Actualizar URL de Render después de despliegue"
git push origin prueva-antes-main
```

---

## 🎯 CHECKLIST POST-DESPLIEGUE

```
□ URL pública: https://agromanager-api.onrender.com
□ Health check: 200 OK
□ Swagger: Funciona
□ Registro: Funciona
□ Login: Recibe JWT token
□ CRUD: Funciona con autorización
□ README.md: Actualizado
□ Última commit: "Despliegue exitoso en Render"
□ GitHub: Cambios pusheados
```

---

## 🎉 DESPUÉS DEL DESPLIEGUE

¡Felicidades! Tu API está en producción. Próximos pasos:

```
1. Agregar ManyToMany en apps (30 min)
2. Mejorar tests de Sensores (30 min)
3. Preparar presentación (2 horas)
4. Ensayar exposición (30 min)
5. ¡LISTO PARA VIERNES 12 DE DICIEMBRE!
```

Ver [CHECKLIST_FINAL.md](CHECKLIST_FINAL.md) para próximos pasos.

---

## 📞 SOPORTE

Si algo falla durante el despliegue:

1. **Revisa logs en Render:** Dashboard → Tu servicio → Logs
2. **Compara con DESPLIEGUE_RENDER.md:** Sección de troubleshooting
3. **Verifica variables de entorno:** Pasos 1-4 de este documento
4. **Intenta "Manual Deploy":** Botón arriba a la derecha

**Tiempo máximo de troubleshooting:** 30 minutos
**Si no funciona después de 30 min:** Revisa que requirements.txt tenga Gunicorn y todo necesario

---

**Última Actualización:** 11 de diciembre de 2025, 23:55  
**Versión:** 1.0 Final  
**Status:** ✅ Listo para usar

¡A DESPLEGAR! 🚀
