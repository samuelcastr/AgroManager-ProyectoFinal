"""
Script de prueba para los endpoints de la API de AgroManager
Ejecutar con: python manage.py shell < test_api.py
"""
from cultivos.models import Cultivo, CicloSiembra, Variedad
from datetime import date, timedelta

# Limpiar datos anteriores
Cultivo.objects.all().delete()
CicloSiembra.objects.all().delete()
Variedad.objects.all().delete()

# Crear variedades
print("✅ Creando variedades...")
var_trigo = Variedad.objects.create(
    nombre="Trigo Blanco Premium",
    descripcion="Variedad de trigo blanco de alta calidad"
)

var_maiz = Variedad.objects.create(
    nombre="Maíz Híbrido Amarillo",
    descripcion="Variedad híbrida de maíz amarillo"
)

var_arroz = Variedad.objects.create(
    nombre="Arroz Largo Blanco",
    descripcion="Variedad de arroz de grano largo"
)

# Crear cultivos
print("✅ Creando cultivos...")
cultivo_trigo = Cultivo.objects.create(
    nombre="Trigo",
    tipo="cereal",
    variedad=var_trigo,
    unidad_productiva="Campo Norte"
)

cultivo_maiz = Cultivo.objects.create(
    nombre="Maíz",
    tipo="cereal",
    variedad=var_maiz,
    unidad_productiva="Campo Sur"
)

cultivo_arroz = Cultivo.objects.create(
    nombre="Arroz",
    tipo="cereal",
    variedad=var_arroz,
    unidad_productiva="Campo Este"
)

cultivo_soja = Cultivo.objects.create(
    nombre="Soja",
    tipo="leguminosa",
    variedad=None,
    unidad_productiva="Campo Oeste"
)

# Crear ciclos de siembra
print("✅ Creando ciclos de siembra...")
hoy = date.today()

# Ciclo activo de Trigo
ciclo_trigo = CicloSiembra.objects.create(
    cultivo=cultivo_trigo,
    fecha_siembra=hoy - timedelta(days=30),
    fecha_cosecha_estimada=hoy + timedelta(days=60),
    estado=CicloSiembra.EN_PROGRESO,
    superficie_hectareas=100.5,
    rendimiento_estimado=2500.0
)

# Ciclo finalizado de Maíz
ciclo_maiz = CicloSiembra.objects.create(
    cultivo=cultivo_maiz,
    fecha_siembra=hoy - timedelta(days=120),
    fecha_cosecha_estimada=hoy - timedelta(days=20),
    estado=CicloSiembra.FINALIZADO,
    superficie_hectareas=150.0,
    rendimiento_estimado=3500.0
)

# Ciclo activo de Arroz
ciclo_arroz = CicloSiembra.objects.create(
    cultivo=cultivo_arroz,
    fecha_siembra=hoy - timedelta(days=45),
    fecha_cosecha_estimada=hoy + timedelta(days=45),
    estado=CicloSiembra.EN_PROGRESO,
    superficie_hectareas=80.0,
    rendimiento_estimado=1800.0
)

# Ciclo activo de Soja
ciclo_soja = CicloSiembra.objects.create(
    cultivo=cultivo_soja,
    fecha_siembra=hoy - timedelta(days=60),
    fecha_cosecha_estimada=hoy + timedelta(days=30),
    estado=CicloSiembra.EN_PROGRESO,
    superficie_hectareas=120.0,
    rendimiento_estimado=2200.0
)

print("\n" + "="*60)
print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
print("="*60)
print(f"\n📊 Resumen:")
print(f"  • Variedades: 3")
print(f"  • Cultivos: 4")
print(f"  • Ciclos activos: 3")
print(f"  • Ciclos finalizados: 1")
print("\n" + "="*60)
print("🚀 Ahora prueba estos endpoints:")
print("="*60)
print("\n1️⃣  LISTAR CULTIVOS:")
print("   GET http://localhost:8000/api/cultivos/")

print("\n2️⃣  FILTRAR CULTIVOS POR NOMBRE:")
print("   GET http://localhost:8000/api/cultivos/?nombre=trigo")

print("\n3️⃣  FILTRAR CULTIVOS POR TIPO:")
print("   GET http://localhost:8000/api/cultivos/?tipo=cereal")

print("\n4️⃣  FILTRAR CULTIVOS POR VARIEDAD:")
print("   GET http://localhost:8000/api/cultivos/?variedad=Blanco")

print("\n5️⃣  BUSCAR CON SEARCH:")
print("   GET http://localhost:8000/api/cultivos/?search=maíz")

print("\n6️⃣  LISTAR CICLOS:")
print("   GET http://localhost:8000/api/ciclos/")

print("\n7️⃣  FILTRAR CICLOS ACTIVOS:")
print("   GET http://localhost:8000/api/ciclos/?estado=EN_PROGRESO")

print("\n8️⃣  FILTRAR CICLOS FINALIZADOS:")
print("   GET http://localhost:8000/api/ciclos/?estado=FINALIZADO")

print("\n9️⃣  FILTRAR POR NOMBRE DE CULTIVO:")
print("   GET http://localhost:8000/api/ciclos/?cultivo__nombre=maíz")

print("\n🔟 RENDIMIENTO PROMEDIO:")
print(f"   GET http://localhost:8000/api/cultivos/{cultivo_trigo.id}/rendimiento_estimado/")

print("\n" + "="*60)
print("🌐 Para iniciar el servidor:")
print("="*60)
print("   python manage.py runserver")
print("\n" + "="*60)
