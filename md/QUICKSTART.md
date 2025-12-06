# ⚡ QUICK START — AgroManager API

## 1️⃣ Instalación Rápida (5 minutos)

```bash
# Clonar
git clone https://github.com/samuelcastr/AgroManager-ProyectoFinal.git
cd AgroManager-ProyectoFinal

# Entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# source venv/bin/activate     # Linux/Mac

# Instalar
pip install -r requirements.txt

# Configurar
cp .env.example .env
# Editar .env si es necesario (DEBUG, DATABASE_URL, etc)

# Base de datos
python manage.py migrate --settings=config.settings.dev

# Usuario admin
python manage.py createsuperuser --settings=config.settings.dev
```

---

## 2️⃣ Iniciar Servidor (1 minuto)

```bash
# Desarrollo
python manage.py runserver --settings=config.settings.dev

# O simplemente (si DJANGO_SETTINGS_MODULE está en .env)
python manage.py runserver
```

**Acceso:**
- 🌐 API: http://localhost:8000/api/
- 📚 Swagger: http://localhost:8000/swagger/
- 👨‍💼 Admin: http://localhost:8000/admin/
- 💚 Health: http://localhost:8000/api/core/health/

---

## 3️⃣ Obtener JWT Token

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"contraseña"}'

# Respuesta
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 4️⃣ Usar Token

```bash
# En cualquier request autenticado
curl -X GET http://localhost:8000/api/core/profiles/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 5️⃣ Ejecutar Tests

```bash
# Todos los tests
python manage.py test apps.core --settings=config.settings.dev

# Un test específico
python manage.py test apps.core.tests.HealthCheckTestCase --settings=config.settings.dev

# Con cobertura
coverage run --source='apps' manage.py test --settings=config.settings.dev
coverage report
```

---

## 6️⃣ Crear Migraciones

```bash
# Hacer cambios en models.py, luego:
python manage.py makemigrations core --settings=config.settings.dev
python manage.py migrate --settings=config.settings.dev
```

---

## 7️⃣ Swagger / Documentación

- 📖 Swagger UI: http://localhost:8000/swagger/
- 📘 ReDoc: http://localhost:8000/redoc/
- 📄 Schema JSON: http://localhost:8000/swagger.json

---

## 8️⃣ Admin Django

- URL: http://localhost:8000/admin/
- Usuario: `admin`
- Modelos: UserProfile, UnidadProductiva, AuditLog

---

## 9️⃣ Filtrado Avanzado

```bash
# Búsqueda
GET /api/core/profiles/?search=juan

# Filtros
GET /api/core/profiles/?role=agricultor&is_verified=true

# Ordenamiento
GET /api/core/profiles/?ordering=-created_at

# Dates
GET /api/core/unidades-productivas/?created_at__gte=2025-01-01
```

---

## 🔟 Próximos Pasos

1. Integrar otra app (usuarios, inventario, cultivos, sensores)
2. Agregar más models/endpoints
3. Escribir tests
4. Hacer PR con referencias a issues
5. Desplegar a producción

---

## ❓ Errores Comunes

### "ModuleNotFoundError: No module named 'apps.core'"
→ Verificar `apps/__init__.py` existe

### "Unable to configure handler 'file'"
→ Ejecutar: `mkdir logs` en raíz

### "Django version mismatch"
→ `pip install -r requirements.txt --force-reinstall`

### JWT token expirado
→ Usar endpoint `/api/auth/refresh/` con refresh_token

---

**¡Listo! Ahora integra tu app 🚀**

