import os
from .base import *

# Desarrollo: DEBUG activado, hosts permisivos
DEBUG = True
ALLOWED_HOSTS = ['*']

# Email backend para desarrollo (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Swagger completo en dev
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
