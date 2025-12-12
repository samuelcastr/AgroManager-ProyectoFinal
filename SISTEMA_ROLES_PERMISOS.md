# 🔐 SISTEMA DE ROLES Y PERMISOS

**Fecha:** 11 de diciembre de 2025  
**Estado:** ✅ Implementado  

---

## 📋 Resumen de Roles

| Rol | Descripción | Puede Crear | Puede Editar | Puede Eliminar | Permisos Especiales |
|-----|------------|-------------|-------------|----------------|-------------------|
| **admin** | Administrador del sistema | Todo | Todo | Todo | Acceso total, gestionar roles |
| **agricultor** | Gestor agrícola | Cultivos, Ciclos | Sus propios datos | Sus propios datos | Crear reportes, ver sensores |
| **distribuidor** | Gestor de inventario | Insumos, Lotes | Inventario | Movimientos | Gestión de stock, reportes |
| **tecnico** | Técnico de campo | Lecturas, Reportes | Lecturas | - | Acceso a sensores, datos en tiempo real |
| **usuario** | Usuario regular | Lectura | Su perfil | Su perfil | Ver datos públicos |

---

## 🔑 Tabla de Permisos Detallada

### APP: core (Usuarios y Autenticación)

```
┌─────────────────────────────┬─────┬────────┬─────┬───────────┬────────┐
│ Acción                      │ Admin│ Agric. │ Dist.│ Técnico   │Usuario │
├─────────────────────────────┼─────┼────────┼─────┼───────────┼────────┤
│ Ver todos los usuarios      │  ✅ │   ❌   │  ❌ │     ❌    │  ❌   │
│ Ver su propio perfil        │  ✅ │   ✅   │  ✅ │     ✅    │  ✅   │
│ Editar su perfil            │  ✅ │   ✅   │  ✅ │     ✅    │  ✅   │
│ Editar perfil de otros      │  ✅ │   ❌   │  ❌ │     ❌    │  ❌   │
│ Cambiar rol de usuario      │  ✅ │   ❌   │  ❌ │     ❌    │  ❌   │
│ Crear unidad productiva     │  ✅ │   ✅   │  ❌ │     ❌    │  ❌   │
│ Editar su unidad productiva │  ✅ │   ✅   │  ❌ │     ❌    │  ❌   │
│ Ver unidades productivas    │  ✅ │   ✅   │  ✅ │     ✅    │  ❌   │
└─────────────────────────────┴─────┴────────┴─────┴───────────┴────────┘
```

### APP: cultivos (Gestión de Cultivos)

```
┌─────────────────────────────┬─────┬────────┬─────┬───────────┬────────┐
│ Acción                      │ Admin│ Agric. │ Dist.│ Técnico   │Usuario │
├─────────────────────────────┼─────┼────────┼─────┼───────────┼────────┤
│ Ver todos los cultivos      │  ✅ │   ✅   │  ❌ │     ✅    │  ❌   │
│ Crear cultivo               │  ✅ │   ✅   │  ❌ │     ❌    │  ❌   │
│ Editar su cultivo           │  ✅ │   ✅   │  ❌ │     ❌    │  ❌   │
│ Editar cultivo de otros     │  ✅ │   ❌   │  ❌ │     ❌    │  ❌   │
│ Eliminar cultivo            │  ✅ │   ✅   │  ❌ │     ❌    │  ❌   │
│ Ver ciclos de siembra       │  ✅ │   ✅   │  ❌ │     ✅    │  ❌   │
│ Crear ciclo de siembra      │  ✅ │   ✅   │  ❌ │     ❌    │  ❌   │
│ Ver rendimiento estimado    │  ✅ │   ✅   │  ❌ │     ✅    │  ❌   │
│ Ver cultivos activos        │  ✅ │   ✅   │  ✅ │     ✅    │  ❌   │
└─────────────────────────────┴─────┴────────┴─────┴───────────┴────────┘
```

### APP: inventario (Gestión de Stock)

```
┌──────────────────────────────┬─────┬────────┬─────┬───────────┬────────┐
│ Acción                       │ Admin│ Agric. │Dist.│ Técnico   │Usuario │
├──────────────────────────────┼─────┼────────┼─────┼───────────┼────────┤
│ Ver todos los insumos        │  ✅ │   ❌   │  ✅ │     ❌    │  ❌   │
│ Crear insumo                 │  ✅ │   ❌   │  ✅ │     ❌    │  ❌   │
│ Editar insumo                │  ✅ │   ❌   │  ✅ │     ❌    │  ❌   │
│ Eliminar insumo              │  ✅ │   ❌   │  ✅ │     ❌    │  ❌   │
│ Ver stock disponible         │  ✅ │   ✅   │  ✅ │     ✅    │  ❌   │
│ Crear lote                   │  ✅ │   ❌   │  ✅ │     ❌    │  ❌   │
│ Registrar entrada de stock   │  ✅ │   ❌   │  ✅ │     ❌    │  ❌   │
│ Registrar salida de stock    │  ✅ │   ✅   │  ✅ │     ✅    │  ❌   │
│ Ver historial de movimientos │  ✅ │   ✅   │  ✅ │     ✅    │  ❌   │
│ Hacer ajuste masivo          │  ✅ │   ❌   │  ✅ │     ❌    │  ❌   │
│ Ver alertas de stock mínimo  │  ✅ │   ❌   │  ✅ │     ❌    │  ❌   │
└──────────────────────────────┴─────┴────────┴─────┴───────────┴────────┘
```

### APP: sensores (Datos en Tiempo Real)

```
┌─────────────────────────────┬─────┬────────┬─────┬───────────┬────────┐
│ Acción                      │ Admin│ Agric. │Dist.│ Técnico   │Usuario │
├─────────────────────────────┼─────┼────────┼─────┼───────────┼────────┤
│ Ver todos los sensores      │  ✅ │   ✅   │  ❌ │     ✅    │  ❌   │
│ Crear sensor                │  ✅ │   ❌   │  ❌ │     ✅    │  ❌   │
│ Editar sensor               │  ✅ │   ❌   │  ❌ │     ✅    │  ❌   │
│ Eliminar sensor             │  ✅ │   ❌   │  ❌ │     ✅    │  ❌   │
│ Ver lecturas                │  ✅ │   ✅   │  ❌ │     ✅    │  ❌   │
│ Crear lectura               │  ✅ │   ❌   │  ❌ │     ✅    │  ❌   │
│ Ver últimas lecturas        │  ✅ │   ✅   │  ❌ │     ✅    │  ❌   │
│ Ver promedio de lecturas    │  ✅ │   ✅   │  ❌ │     ✅    │  ❌   │
│ Exportar datos de sensores  │  ✅ │   ✅   │  ❌ │     ✅    │  ❌   │
└─────────────────────────────┴─────┴────────┴─────┴───────────┴────────┘
```

---

## 🔐 Permisos Globales

### Health Check (`/api/core/health/`)

```
Permiso: AllowAny (Anónimo)
Razón: Monitoreo de aplicación y CI/CD
Respuesta: {status, server, database}
```

### Autenticación (`/api/auth/`)

```
/login/       - AllowAny (Anónimo)
/refresh/     - AllowAny (Token válido)
/register/    - AllowAny (Anónimo) ← Pide rol al registrar
/password-reset/ - AllowAny (Anónimo)
```

### Admin Django (`/admin/`)

```
Permiso: IsAdminUser (staff=True)
Acceso: Solo administradores del sistema
```

### Swagger (`/api/schema/swagger/`)

```
Permiso: AllowAny
Razón: Documentación pública
```

---

## 🛡️ Política de Control de Acceso

### Por Vista (ViewSet)

```python
# Core - UserProfileViewSet
list    → IsAuthenticated
create  → IsAdminUser
retrieve → IsAdminOrOwner
update  → IsAdminOrOwner
destroy → IsAdminOrOwner

# Cultivos - CultivoViewSet
list    → IsAgricultor
create  → IsAgricultor
retrieve → IsAgricultor
update  → IsAgricultor (solo su cultivo)
destroy → IsAgricultor (solo su cultivo)

# Inventario - InsumoViewSet
list    → IsDistribuidor
create  → IsDistribuidor
retrieve → IsDistribuidorOrAdmin
update  → IsDistribuidor
destroy → IsDistribuidor

# Sensores - SensorViewSet
list    → IsTecnico
create  → IsTecnico
retrieve → IsTecnico
update  → IsTecnico (solo sus sensores)
destroy → IsTecnico
```

### Filtrado Automático

```python
# Los usuarios solo ven sus propios datos
def get_queryset(self):
    if not self.request.user.is_staff:
        if hasattr(self.model, 'owner'):
            return self.model.objects.filter(owner=self.request.user)
        if hasattr(self.model, 'user'):
            return self.model.objects.filter(user=self.request.user)
    return self.model.objects.all()
```

---

## 📝 Ciclo de Registro

### Proceso de Registro con Rol

```
1. Usuario accede a POST /api/auth/register/
   ↓
2. Completa formulario:
   - username (único)
   - email (único)
   - password (8+ chars, mayús, minús, números, símbolos)
   - password2 (confirmación)
   - first_name
   - last_name
   - role ← AQUÍ ELIGE SU ROL
   - phone (opcional)
   ↓
3. Sistema valida:
   ✅ Contraseña segura
   ✅ Email único
   ✅ Username único
   ✅ Rol válido
   ↓
4. Se crea:
   - User (usuario Django)
   - UserProfile (con rol especificado)
   ↓
5. Respuesta 201:
   {
     "message": "Usuario registrado exitosamente",
     "user": {
       "id": 123,
       "username": "juan_perez",
       "email": "juan@example.com",
       "first_name": "Juan",
       "last_name": "Pérez",
       "role": "agricultor",
       "phone": "+57 310 123 4567"
     }
   }
```

---

## 🔄 Cambio de Rol

### Solo Administrador Puede Cambiar Rol

```bash
PATCH /api/core/users/{id}/
Authorization: Bearer ADMIN_TOKEN
Content-Type: application/json

{
  "role": "tecnico"  # Cambiar de agricultor a técnico
}

Respuesta: 200 OK
{
  "message": "Rol actualizado a: tecnico"
}
```

---

## 🚨 Violaciones de Permisos

### Intentar acceder sin permiso

```bash
GET /api/cultivos/
Authorization: Bearer DISTRIBUIDOR_TOKEN

Respuesta: 403 Forbidden
{
  "detail": "No tienes permiso para acceder a este recurso",
  "code": "permission_denied"
}
```

### Intentar editar dato de otro usuario

```bash
PATCH /api/core/users/456/
Authorization: Bearer USER_ID_123_TOKEN

Respuesta: 403 Forbidden
{
  "detail": "Solo puedes editar tus propios datos",
  "code": "permission_denied"
}
```

---

## 📊 Matriz de Permisos Resumida

```
ADMIN       → Acceso total a todo ✅
AGRICULTOR  → Cultivos + sensores + inventario (lectura) ✅
DISTRIBUIDOR → Inventario + sensores (lectura) ✅
TECNICO     → Sensores + datos en tiempo real ✅
USUARIO     → Lectura de datos públicos ✅
```

---

## 🔑 Variables de Entorno de Seguridad

```env
DEBUG=False                    # Nunca True en producción
SECRET_KEY=CAMBIAR-PERIODICAMENTE
ALLOWED_HOSTS=api.tudominio.com,www.api.tudominio.com
CSRF_TRUSTED_ORIGINS=https://frontend.tudominio.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## ✅ Checklist de Seguridad

- [ ] DEBUG=False en producción
- [ ] SECRET_KEY cambiadoriódicamente
- [ ] HTTPS forzado en producción
- [ ] CSRF protection habilitada
- [ ] Passwords hasheadas (argon2)
- [ ] JWT tokens con expiración
- [ ] Logs de acceso configurados
- [ ] Rate limiting implementado (pendiente)
- [ ] CORS configurado correctamente
- [ ] Validación en todos los serializers

---

## 📝 Logs de Auditoría

Cada cambio importante se registra:

```
✅ Nuevo usuario registrado: username=juan, role=agricultor
✅ Login: user=juan (IP: 192.168.1.1)
✅ Cultivo creado: cultivo_id=5, owner=juan
✅ Stock salida: insumo_id=3, cantidad=50, usuario=distribuidor
✅ Lectura de sensor: sensor_id=1, valor=23.5C
❌ Login fallido: username=juan (3 intentos consecutivos)
```

---

## 🎯 Implementación Técnica

### En views.py

```python
# Aplicar permisos a ViewSet
class CultivoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAgricultor]
    
    def get_permissions(self):
        """Permisos granulares por acción"""
        if self.action == 'list':
            permission_classes = [IsAgricultor]
        elif self.action == 'create':
            permission_classes = [IsAgricultor]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAgricultor, IsOwner]
        return [permission() for permission in permission_classes]
```

### En serializers.py

```python
# Validación en serializer
class CultivoSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # Solo agricultores pueden crear cultivos
        if self.context['request'].user.profile.role != 'agricultor':
            raise ValidationError("Solo agricultores pueden crear cultivos")
        return data
```

---

**Generado:** 11 de diciembre de 2025  
**Estado:** ✅ Completamente implementado  
**Próximo:** Despliegue en Render
