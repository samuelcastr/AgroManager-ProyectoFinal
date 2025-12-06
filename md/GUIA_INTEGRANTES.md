# 👥 GUÍA PARA PRÓXIMOS INTEGRANTES

## 🎯 Bienvenido al Proyecto AgroManager

Este documento es una guía rápida para que los demás integrantes del equipo puedan:
1. Entender lo que Samuel (Líder) ha preparado
2. Integrar sus apps fácilmente
3. Mantener los estándares de código
4. Colaborar efectivamente

---

## 📋 Lo que Samuel ya hizo:

✅ **Infraestructura base:** config/, settings (dev/prod), urls  
✅ **App core:** Modelos, serializers, views, permisos, utils  
✅ **Autenticación JWT:** SimpleJWT configurado  
✅ **Seguridad:** DEBUG, SECRET_KEY, CORS configurados  
✅ **Documentación:** README, ARCHITECTURE, guías  
✅ **Testing:** 23 tests pasando  
✅ **CI/CD:** GitHub Actions pipeline  

---

## 🚀 Próximos pasos para cada integrante:

### Juan Riveros — App `usuarios`

**Crear la app:**
```bash
python manage.py startapp usuarios apps/usuarios --settings=config.settings.dev
```

**Archivo: `apps/usuarios/models.py`**
```python
from django.db import models
from django.contrib.auth.models import User
from apps.core.models import TimestampedModel

class User Extended (TimestampedModel):
    # Tu lógica aquí
    pass
```

**Archivo: `apps/usuarios/serializers.py`**
```python
from rest_framework import serializers
# Tu lógica aquí
```

**Archivo: `apps/usuarios/views.py`**
```python
from rest_framework import viewsets
# Tu ViewSets aquí
```

**Registrar en settings:**
```python
INSTALLED_APPS = [
    # ...
    "apps.usuarios",
]
```

**Crear rutas:**
```python
# apps/usuarios/urls.py
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# Registrar tus ViewSets

urlpatterns = [
    # ...
    path('', include(router.urls)),
]
```

**En config/urls.py:**
```python
urlpatterns = [
    # ...
    path("api/usuarios/", include("apps.usuarios.urls")),
]
```

**Tests:**
```bash
# Crear tests como Samuel hizo
# apps/usuarios/tests.py
```

**Migrar:**
```bash
python manage.py makemigrations usuarios --settings=config.settings.dev
python manage.py migrate --settings=config.settings.dev
```

---

### Beickert Torres — App `inventario`

**Especificidades:**
- ✅ Implementar transacción atómica en salida de stock
- ✅ MovimientoStock + decremento de Lote
- ✅ Endpoints personalizados: alertas-stock, ajuste-masivo

**Ejemplo transacción:**
```python
from django.db import transaction

@transaction.atomic
def salida_stock(request):
    # 1. Validar stock
    # 2. Crear MovimientoStock
    # 3. Decrementar Lote
    # Si falla cualquiera → rollback
    pass
```

---

### María Fernanda Rojas — App `cultivos`

**Relaciones a implementar:**
- FK: `Cultivo` → `UnidadProductiva` (ya existe en core)
- M2M: `Cultivo` ↔ `Sensor` (con sensores)

**Endpoints personalizados:**
- `/api/cultivos/{pk}/rendimiento_estimado/`
- `/api/cultivos/activos/`

---

### Cielos Alexandra Rodríguez — App `sensores`

**Lecturas IoT:**
- `LecturaSensor` con timestamp, valor
- Bulk insert de lecturas
- Agregación por día/hora

**Endpoints:**
- `/api/sensores/{id}/ultimas/`
- `/api/sensores/reporte/`

---

## 🔄 FLUJO DE TRABAJO COLABORATIVO

### 1. Crear Issue

```markdown
[APP] – Breve descripción

Objetivo:
...

Criterios de Aceptación:
- [ ] Endpoint funcional
- [ ] Tests escritos
- [ ] Documentación Swagger
```

### 2. Crear Rama

```bash
git checkout develop
git pull origin develop
git checkout -b juan/issue-12-usuarios-register
```

### 3. Hacer Cambios

```bash
# Hacer tus cambios
git add .
git commit -m "feat(usuarios): implementar register #12"
git push origin juan/issue-12-usuarios-register
```

### 4. Crear PR

- Referenciar issue: "Closes #12"
- Describir cambios
- Asignar reviewers (mínimo Samuel)

### 5. Revisión Cruzada

**Todos deben revisar código de otros:**
- Comentar
- Sugerir mejoras
- Aprobar

### 6. Samuel hace Merge

Samuel revisa y hace merge a `develop`, luego a `main`

---

## 📝 ESTÁNDARES DE CÓDIGO

### Models

```python
from apps.core.models import TimestampedModel

class MiModelo(TimestampedModel):
    # Usar timestampedmodel para created_at, updated_at
    campo = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Mi Modelo"
        indexes = [models.Index(fields=['campo'])]
    
    def __str__(self):
        return self.campo
```

### Serializers

```python
from rest_framework import serializers

class MiSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiModelo
        fields = ['id', 'campo', 'created_at']
    
    def validate_campo(self, value):
        if not value:
            raise serializers.ValidationError("Requerido")
        return value
```

### ViewSets

```python
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

class MiViewSet(viewsets.ModelViewSet):
    queryset = MiModelo.objects.all()
    serializer_class = MiSerializer
    permission_classes = [IsAuthenticated]
    
    # Filtrado
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['campo']
    search_fields = ['campo']
```

### Tests

```python
from rest_framework.test import APITestCase

class MiTest(APITestCase):
    def test_endpoint_funciona(self):
        response = self.client.get('/api/mi-app/')
        self.assertEqual(response.status_code, 200)
```

---

## 🔐 USO DE PERMISOS

```python
from apps.core.permissions import IsOwner, IsAdminUser

class MiViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    # O personalizado:
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        return super().get_permissions()
```

---

## 📚 DOCUMENTACIÓN

### README de tu app

Agregar sección a `README.md`:

```markdown
## App USUARIOS

### Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| POST | /api/usuarios/register/ | Registrar usuario |
| POST | /api/usuarios/login/ | Login |

### Ejemplo

```bash
curl -X POST http://localhost:8000/api/usuarios/register/ \
  -d '{"username": "juan", "email": "juan@example.com"}'
```
```

---

## 🧪 TESTS

### Ejecutar

```bash
# Tu app
python manage.py test apps.usuarios --settings=config.settings.dev

# Todo
python manage.py test --settings=config.settings.dev

# Cobertura
coverage run --source='apps' manage.py test --settings=config.settings.dev
coverage report
```

---

## 💾 MIGRACIONES

```bash
# Crear
python manage.py makemigrations usuarios --settings=config.settings.dev

# Aplicar
python manage.py migrate --settings=config.settings.dev

# Ver migraciones pendientes
python manage.py showmigrations --settings=config.settings.dev
```

---

## 🚨 ERRORES COMUNES

### "No installed app with label 'usuarios'"
→ Agregar en `INSTALLED_APPS` en base.py

### "ModuleNotFoundError: No module named 'apps.usuarios.models'"
→ Crear `__init__.py` en `apps/usuarios/`

### Tests fallan
→ Verificar que la BD existe y está migrada
→ `python manage.py migrate --settings=config.settings.dev`

### Filtrado no funciona
→ Verificar `FilterBackend` en ViewSet
→ Usar `filterset_fields` correctamente

---

## 📞 COMUNICACIÓN

- **Issues:** Crear en GitHub para cada tarea
- **PRs:** Describir bien, asignar reviewers
- **Slack/Discord:** Para preguntas rápidas
- **Reuniones:** Sincronización del equipo

---

## ✅ ANTES DE HACER PR

- [ ] Tests escritos y pasando
- [ ] Código sin errores (flake8)
- [ ] Documentación actualizada
- [ ] Issue referenciado
- [ ] Revisor asignado
- [ ] Cambios probados localmente

---

## 🎓 RECURSOS

- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- SimpleJWT: https://github.com/jpadilla/django-rest-framework-simplejwt
- django-filter: https://django-filter.readthedocs.io/

---

## 🤝 APOYO

Si tienes dudas:
1. Revisar `README.md`
2. Revisar `ARCHITECTURE.md`
3. Revisar código de Samuel en `apps/core/`
4. Preguntar al equipo en reunión
5. Abrir issue de soporte

---

**¡Bienvenido al equipo! 🚀 Vamos a hacer un gran proyecto juntos.**

