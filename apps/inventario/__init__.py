# Lightweight shim package to make the app importable as "inventario" for Django settings.
# It forwards to the real package under apps.inventario
from importlib import import_module

_mod = import_module('apps.inventario')
# Expose public names (models, apps, etc.) if needed by Django
for _name in dir(_mod):
    if not _name.startswith('_'):
        globals()[_name] = getattr(_mod, _name)
