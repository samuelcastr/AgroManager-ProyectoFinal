import os
from .base import *
from decouple import config


# Development database overrides (use environment via python-decouple)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }

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
