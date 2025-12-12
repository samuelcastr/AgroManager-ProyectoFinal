#!/usr/bin/env python
"""
Script para configurar PostgreSQL para AgroManager
Uso: python setup_postgresql.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(text):
    """Imprime un encabezado"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def check_postgresql():
    """Verifica si PostgreSQL está instalado"""
    print_header("1. Verificando PostgreSQL")
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ PostgreSQL encontrado: {result.stdout.strip()}")
            return True
        else:
            print("✗ PostgreSQL no encontrado")
            print("  Descarga desde: https://www.postgresql.org/download/")
            return False
    except Exception as e:
        print(f"✗ Error al verificar PostgreSQL: {e}")
        return False

def check_psycopg2():
    """Verifica si psycopg2 está instalado"""
    print_header("2. Verificando psycopg2")
    try:
        import psycopg2
        print(f"✓ psycopg2 instalado: versión {psycopg2.__version__}")
        return True
    except ImportError:
        print("✗ psycopg2 no instalado")
        print("  Ejecuta: pip install psycopg2-binary==2.9.9")
        return False

def test_postgresql_connection(user, password, host='localhost', port='5432'):
    """Prueba la conexión a PostgreSQL"""
    print_header("3. Probando conexión a PostgreSQL")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'
        )
        conn.close()
        print(f"✓ Conexión exitosa a PostgreSQL")
        print(f"  Host: {host}:{port}")
        print(f"  Usuario: {user}")
        return True
    except psycopg2.OperationalError as e:
        print(f"✗ No se puede conectar a PostgreSQL: {e}")
        return False

def create_database(user, password, host='localhost', port='5432'):
    """Crea la base de datos y usuario"""
    print_header("4. Creando base de datos")
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Crear BD
        try:
            cursor.execute("CREATE DATABASE agromanager_db;")
            print("✓ Base de datos 'agromanager_db' creada")
        except psycopg2.Error as e:
            if 'already exists' in str(e):
                print("⚠ Base de datos 'agromanager_db' ya existe")
            else:
                raise
        
        # Crear usuario (opcional)
        try:
            cursor.execute("CREATE USER agromanager_user WITH PASSWORD 'agromanager_pass';")
            print("✓ Usuario 'agromanager_user' creado")
        except psycopg2.Error as e:
            if 'already exists' in str(e):
                print("⚠ Usuario 'agromanager_user' ya existe")
            else:
                raise
        
        # Dar permisos
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE agromanager_db TO agromanager_user;")
        print("✓ Permisos asignados")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Error al crear base de datos: {e}")
        return False

def run_migrations():
    """Ejecuta las migraciones de Django"""
    print_header("5. Aplicando migraciones de Django")
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'migrate', '--settings=config.settings.dev'],
            cwd=str(Path(__file__).parent),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Migraciones aplicadas exitosamente")
            print("\nSalida:")
            print(result.stdout)
            return True
        else:
            print("✗ Error al aplicar migraciones")
            print("\nErrores:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def create_superuser():
    """Crea un superusuario"""
    print_header("6. Creando superusuario (opcional)")
    try:
        print("Ejecuta: python manage.py createsuperuser --settings=config.settings.dev")
        print("O más tarde accede a: http://localhost:8000/admin/")
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def generate_summary():
    """Genera un resumen de la configuración"""
    print_header("RESUMEN DE CONFIGURACION")
    
    config = {
        "Base de Datos": {
            "Engine": "PostgreSQL",
            "Database": "agromanager_db",
            "User": "postgres",
            "Host": "localhost",
            "Port": "5432"
        },
        "Proximos Pasos": [
            "1. Verifica que PostgreSQL esté ejecutándose",
            "2. Instala DBeaver (opcional): https://dbeaver.io/",
            "3. Inicia el servidor: python manage.py runserver --settings=config.settings.dev",
            "4. Accede a: http://localhost:8000/swagger/"
        ],
        "Pruebas Recomendadas": [
            "GET /api/core/health/ - Verificar conexión",
            "POST /api/auth/register/ - Registrar usuario",
            "POST /api/auth/login/ - Obtener JWT token",
            "POST /api/cultivos/ - Crear cultivo"
        ]
    }
    
    print(json.dumps(config, indent=2, ensure_ascii=False))

def main():
    """Función principal"""
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  CONFIGURACION DE POSTGRESQL PARA AGROMANAGER".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    # Verificaciones
    if not check_postgresql():
        return
    
    if not check_psycopg2():
        print("\n⚠ Instala psycopg2 primero:")
        print("  pip install psycopg2-binary==2.9.9")
        return
    
    # Credenciales por defecto
    pg_user = "postgres"
    pg_password = "postgres"
    pg_host = "localhost"
    pg_port = "5432"
    
    print("\nUsando credenciales por defecto de PostgreSQL:")
    print(f"  Usuario: {pg_user}")
    print(f"  Host: {pg_host}:{pg_port}")
    
    # Probar conexión
    if not test_postgresql_connection(pg_user, pg_password, pg_host, pg_port):
        print("\n⚠ No se puede conectar a PostgreSQL con las credenciales por defecto")
        print("  Verifica que PostgreSQL esté ejecutándose e intenta de nuevo")
        return
    
    # Crear BD
    if not create_database(pg_user, pg_password, pg_host, pg_port):
        return
    
    # Aplicar migraciones
    if not run_migrations():
        return
    
    # Crear superusuario
    create_superuser()
    
    # Resumen
    generate_summary()
    
    print("\n" + "="*80)
    print("✓ CONFIGURACION COMPLETADA")
    print("="*80)
    print("\nInicia el servidor con:")
    print("  python manage.py runserver --settings=config.settings.dev")

if __name__ == '__main__':
    main()
