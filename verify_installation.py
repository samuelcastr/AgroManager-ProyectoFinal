#!/usr/bin/env python
"""
Script de verificación de instalación para AgroManager API
Ejecutar: python verify_installation.py
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(path, name):
    """Verificar si un archivo existe"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {name}")
    return exists

def check_module_installed(module_name, display_name):
    """Verificar si un módulo Python está instalado"""
    try:
        __import__(module_name)
        print(f"✅ {display_name}")
        return True
    except ImportError:
        print(f"❌ {display_name}")
        return False

def main():
    print("\n" + "="*60)
    print("🔍 VERIFICACIÓN DE INSTALACIÓN - AgroManager API")
    print("="*60 + "\n")

    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent

    checks = {
        "Archivos de Configuración": [
            ("config/settings/base.py", "Config base"),
            ("config/settings/dev.py", "Config desarrollo"),
            ("config/settings/prod.py", "Config producción"),
            ("config/urls.py", "URLs principales"),
            ("config/wsgi.py", "WSGI"),
            ("config/swagger.py", "Swagger config"),
        ],
        "App CORE": [
            ("apps/core/models.py", "Modelos"),
            ("apps/core/serializers.py", "Serializers"),
            ("apps/core/views.py", "Views"),
            ("apps/core/permissions.py", "Permisos"),
            ("apps/core/exceptions.py", "Exception handler"),
            ("apps/core/utils.py", "Utilidades"),
            ("apps/core/admin.py", "Admin"),
            ("apps/core/tests.py", "Tests"),
            ("apps/core/urls.py", "URLs"),
        ],
        "Migraciones": [
            ("apps/core/migrations/0001_initial.py", "Migraciones"),
            ("db.sqlite3", "Base de datos"),
        ],
        "Documentación": [
            ("README.md", "README"),
            ("ARCHITECTURE.md", "Arquitectura"),
            ("DELIVERY_SUMMARY.md", "Resumen entrega"),
            ("CHECKLIST_SAMUEL.md", "Checklist"),
            ("QUICKSTART.md", "Quick start"),
        ],
        "DevOps": [
            ("requirements.txt", "Dependencies"),
            (".env.example", "Env example"),
            (".github/workflows/ci.yml", "CI/CD pipeline"),
            (".github/ISSUE_TEMPLATE/feature.md", "Issue template"),
            (".gitignore", "Git ignore"),
        ],
    }

    total_files = 0
    files_found = 0

    for section, files in checks.items():
        print(f"\n📁 {section}")
        print("-" * 60)
        for file_path, name in files:
            full_path = project_root / file_path
            if check_file_exists(full_path, name):
                files_found += 1
            total_files += 1

    print(f"\n\n📊 ARCHIVO: {files_found}/{total_files} archivos ✅\n")

    # Verificar módulos Python
    print("="*60)
    print("📦 MÓDULOS PYTHON INSTALADOS")
    print("="*60 + "\n")

    modules = [
        ("django", "Django"),
        ("rest_framework", "Django REST Framework"),
        ("rest_framework_simplejwt", "SimpleJWT"),
        ("corsheaders", "CORS Headers"),
        ("drf_yasg", "Swagger"),
        ("django_filters", "Django Filter"),
        ("dotenv", "Python Dotenv"),
        ("psycopg2", "psycopg2 (PostgreSQL)"),
        ("sentry_sdk", "Sentry SDK"),
    ]

    modules_found = 0
    for module, display_name in modules:
        if check_module_installed(module, display_name):
            modules_found += 1
        total_files += 1

    print(f"\n✅ MÓDULOS: {modules_found}/{len(modules)} instalados\n")

    # Verificar superusuario
    print("="*60)
    print("👤 VERIFICACIÓN DE BASE DE DATOS")
    print("="*60 + "\n")

    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
        django.setup()

        from django.contrib.auth.models import User
        from apps.core.models import UserProfile

        admin_users = User.objects.filter(is_superuser=True).count()
        profiles = UserProfile.objects.count()

        print(f"✅ Superusuarios: {admin_users}")
        print(f"✅ Perfiles: {profiles}")

        if admin_users > 0:
            print("\n✅ Base de datos lista para usar\n")
        else:
            print("\n⚠️  Crear superusuario: python manage.py createsuperuser --settings=config.settings.dev\n")

    except Exception as e:
        print(f"⚠️  No se pudo verificar BD: {str(e)}\n")

    # Resumen final
    print("="*60)
    print("✨ RESUMEN FINAL")
    print("="*60 + "\n")

    if files_found == total_files - len(modules) and modules_found >= len(modules) - 2:
        print("✅ PROYECTO LISTO PARA USAR")
        print("\n🚀 Siguientes pasos:")
        print("   1. python manage.py runserver --settings=config.settings.dev")
        print("   2. Acceder a http://localhost:8000/swagger/")
        print("   3. Login con admin / contraseña")
        print("   4. Comenzar desarrollo\n")
        return 0
    else:
        print("⚠️  Algunas cosas falta completar")
        print("\n📝 Instrucciones:")
        print("   1. pip install -r requirements.txt")
        print("   2. python manage.py migrate --settings=config.settings.dev")
        print("   3. python manage.py createsuperuser --settings=config.settings.dev\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
