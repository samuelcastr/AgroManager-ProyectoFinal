import os
from .base import *

# Desarrollo: DEBUG activado, hosts permisivos
DEBUG = True
ALLOWED_HOSTS = ['*']

# Cambiar entre SQLite (rapido) y PostgreSQL (produccion)
USE_POSTGRESQL = False  # Cambiar a True cuando PostgreSQL esté corriendo

if USE_POSTGRESQL:
    # Development database: PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'agromanager',  # Nombre de la base de datos
            'USER': 'postgres',  # Usuario de PostgreSQL
            'PASSWORD': 'postgres',  # Contraseña
            'HOST': 'localhost',  # Servidor
            'PORT': '5432',  # Puerto por defecto
        }
    }
else:
    # Desarrollo rápido: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
        }
    }

# Email backend para desarrollo (console - muestra en terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@agromanager.local'

# Swagger settings para desarrollo
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': True,
}
