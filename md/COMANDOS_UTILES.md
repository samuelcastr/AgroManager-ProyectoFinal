# 🚀 Comandos Útiles - AgroManager API

## Servidor

```bash
# Iniciar servidor en desarrollo
python manage.py runserver --settings=config.settings.dev

# Servidor en puerto específico
python manage.py runserver 0.0.0.0:8001 --settings=config.settings.dev
```

## Base de Datos

```bash
# Ver migraciones pendientes
python manage.py showmigrations --settings=config.settings.dev

# Crear migraciones
python manage.py makemigrations --settings=config.settings.dev

# Aplicar migraciones
python manage.py migrate --settings=config.settings.dev

# Revertir última migración
python manage.py migrate apps.core 0001 --settings=config.settings.dev

# Ver estado de una app
python manage.py showmigrations apps.core --settings=config.settings.dev
```

## Usuario

```bash
# Crear superusuario
python manage.py createsuperuser --settings=config.settings.dev

# Cambiar contraseña
python manage.py changepassword <username> --settings=config.settings.dev

# Crear usuario regular
python manage.py shell --settings=config.settings.dev
# En la consola:
# from django.contrib.auth.models import User
# User.objects.create_user('username', 'email@example.com', 'password')
```

## Tests

```bash
# Ejecutar todos los tests
python manage.py test --settings=config.settings.dev

# Tests con verbose
python manage.py test --settings=config.settings.dev -v 2

# Tests específicos de una app
python manage.py test apps.core --settings=config.settings.dev

# Tests específicos de una clase
python manage.py test apps.core.tests.RegisterAPITestCase --settings=config.settings.dev

# Tests específicos de un método
python manage.py test apps.core.tests.RegisterAPITestCase.test_register_user_success --settings=config.settings.dev

# Tests con coverage
coverage run --source='.' manage.py test --settings=config.settings.dev
coverage report
coverage html
```

## Shell Django

```bash
# Entrar a la consola interactiva
python manage.py shell --settings=config.settings.dev

# Dentro del shell:
from django.contrib.auth.models import User
from apps.core.models import UserProfile, PasswordResetToken

# Crear usuario
user = User.objects.create_user('juan', 'juan@example.com', 'pass123')

# Crear perfil
profile = UserProfile.objects.create(user=user, phone='+573123456789', role='agricultor')

# Ver tokens de recuperación
tokens = PasswordResetToken.objects.all()
for token in tokens:
    print(f"{token.user.username}: {token.is_valid()}")

# Crear token de prueba
reset_token = PasswordResetToken.create_token(user)
print(f"Token: {reset_token.token}")
```

## Linting y Formateo

```bash
# Verificar sintaxis de Python
python -m py_compile apps/core/models.py

# Ejecutar linter (si está instalado)
flake8 apps/core/

# Formatear código (black, si está instalado)
black apps/core/
```

## Utilidades

```bash
# Recopilar archivos estáticos
python manage.py collectstatic --settings=config.settings.prod

# Verificar configuración
python manage.py check --settings=config.settings.dev

# Ver URLs disponibles
python manage.py show_urls --settings=config.settings.dev

# Hacer dump de datos
python manage.py dumpdata apps.core > backup.json --settings=config.settings.dev

# Cargar datos
python manage.py loaddata backup.json --settings=config.settings.dev

# Limpiar datos de una app
python manage.py flush apps.core --settings=config.settings.dev
```

## Git

```bash
# Ver estado
git status

# Ver cambios
git diff

# Agregar cambios
git add .

# Commit
git commit -m "Implementar autenticación: registro y recuperación de contraseña"

# Push
git push origin main

# Ver historial
git log --oneline
```

## cURL - Ejemplos rápidos

```bash
# Registrar usuario
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"juan","email":"juan@example.com","password":"Pass123!","password2":"Pass123!","first_name":"Juan","last_name":"Pérez"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"juan","password":"Pass123!"}'

# Ver perfil (con token)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/core/profiles/me/

# Solicitar recuperación
curl -X POST http://localhost:8000/api/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email":"juan@example.com"}'

# Health check
curl http://localhost:8000/api/core/health/
```

## Python - Verificación rápida

```python
# Verificar instalación de dependencias
python -c "import django; print(f'Django {django.get_version()}')"
python -c "import rest_framework; print(f'DRF {rest_framework.__version__}')"
python -c "from rest_framework_simplejwt import __version__; print(f'SimpleJWT {__version__}')"

# Ver variables de entorno
python -c "import os; print('SECRET_KEY' in os.environ)"

# Verificar BD
python -c "from django.db import connection; print(connection.settings_dict['ENGINE'])"
```

## Troubleshooting

```bash
# Verificar que todo esté bien
python manage.py check --settings=config.settings.dev

# Ver errores en migraciones
python manage.py migrate --plan --settings=config.settings.dev

# Limpiar cache de Python
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Reiniciar servidor sin caché
python manage.py runserver --clear-cache --settings=config.settings.dev
```

## Producción

```bash
# Recopilar estáticos
python manage.py collectstatic --noinput --settings=config.settings.prod

# Ejecutar migraciones
python manage.py migrate --settings=config.settings.prod

# Crear superusuario
python manage.py createsuperuser --settings=config.settings.prod

# Gunicorn (web server)
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --settings=config.settings.prod

# Con workers y timeouts
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120 \
  --settings=config.settings.prod
```

## Desarrollo Rápido

```bash
# Alias útil (agregar a .bashrc o .zshrc)
alias serve='python manage.py runserver --settings=config.settings.dev'
alias migrate='python manage.py migrate --settings=config.settings.dev'
alias makemig='python manage.py makemigrations --settings=config.settings.dev'
alias shell='python manage.py shell --settings=config.settings.dev'
alias test='python manage.py test apps.core.tests --settings=config.settings.dev -v 2'

# Luego usar:
serve
migrate
makemig
shell
test
```

---

**Última actualización:** 5 de diciembre de 2025
