import os
from .base import *

# Desarrollo: DEBUG activado, hosts permisivos
DEBUG = True
ALLOWED_HOSTS = ['*']

# Development database: SQLite (simple para desarrollo)
# Si necesitas MySQL, descomentar y configurar
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
#     }
# }

# Email backend para desarrollo (console - muestra en terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'service@agromanager.local'

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
