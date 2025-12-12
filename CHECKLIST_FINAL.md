# ⏱️ CHECKLIST DE ÚLTIMAS 24 HORAS

**Hora de Inicio:** 11 de diciembre, ~23:45  
**Deadline Final:** Viernes 12 de diciembre, 00:00  
**Tiempo Disponible:** ~24 horas  

---

## 🔴 CRÍTICO (MÁXIMA PRIORIDAD) — 1 HORA

### ✅ Ya completado en sesión anterior:
- [x] Sistema de roles refactorizado
- [x] Permisos granulares por rol
- [x] RegisterSerializer con campo role
- [x] Password validation mejorada
- [x] Procfile para Render creado
- [x] Documentación de Render (DESPLIEGUE_RENDER.md)
- [x] Todo commiteado en GitHub

### 🔴 FALTA AHORA:

#### Tarea 1: DESPLIEGUE EN RENDER
**Tiempo:** 45 minutos  
**Status:** 95% documentado, 0% ejecutado

```
SUBTAREAS:
□ Ir a render.com
□ Crear cuenta (si no existe)
□ Conectar GitHub repo (AgroManager-ProyectoFinal)
□ Crear nuevo Web Service
□ Nombre: agromanager-api
□ Region: North America (Oregon)
□ Plan: Free (o Starter)
□ Conectar deploy branch: prueva-antes-main
□ Agregar variables de entorno:
  - DJANGO_SETTINGS_MODULE = config.settings.prod
  - DEBUG = False
  - SECRET_KEY = (generar nueva con Django secret key generator)
  - DATABASE_URL = (copiar de Railway)
  - ALLOWED_HOSTS = agromanager-api.onrender.com,localhost
  - CORS_ALLOWED_ORIGINS = https://agromanager-api.onrender.com
□ Build Command: (Render automáticamente usa Procfile)
□ Start Command: web (de Procfile)
□ Iniciar Deploy
□ Esperar ~5 minutos a que build termine
□ Verificar que URL esté lista
□ Probar health check: GET /api/core/health/
□ Probar login: POST /api/auth/login/
□ Documentar URL en README.md
□ ¡LISTO PARA PRODUCCIÓN!
```

**Referencia:** Ver [DESPLIEGUE_RENDER.md](DESPLIEGUE_RENDER.md)

---

## ⚠️ IMPORTANTE (DESPUÉS DEL DESPLIEGUE) — 1 HORA

### Tarea 2: Finalizar ManyToMany en cada App
**Tiempo:** 30 minutos  
**Status:** Identificado, no implementado

```
CORE APP:
□ Modelo UnidadProductiva con M2M a User (asignar técnicos)
□ Migración
□ Actualizar serializer

CULTIVOS APP:
□ Modelo Cultivo con M2M a User (operarios)
□ Modelo Ciclo de Siembra (si no existe)
□ Migración
□ Actualizar serializer y viewset

INVENTARIO APP:
□ Modelo Insumo con M2M a Proveedor
□ Modelo Movimiento con M2M a Insumo
□ Migración
□ Actualizar serializer

SENSORES APP:
□ Modelo Sensor con M2M a Ubicación
□ Migración
□ Actualizar serializer y viewset
```

### Tarea 3: Mejorar Tests de Sensores
**Tiempo:** 30 minutos  
**Status:** 1 test básico, necesita 5+

```
TESTS NECESARIOS:
□ Test para SensorSerializer (validación)
□ Test para SensorViewSet.list() (solo usuarios con rol técnico)
□ Test para SensorViewSet.create() (solo admin puede crear)
□ Test para SensorViewSet.update() (solo propietario o admin)
□ Test para SensorViewSet.delete() (solo admin)
□ Test para LecturaSensor (crear lecturas)
□ Test para filtrado por sensor_id

COBERTURA MÍNIMA: 50%+
COMANDO: python manage.py test apps.sensores -v 2
```

---

## 🎬 PREPARACIÓN PARA EXPOSICIÓN (2 HORAS)

### Tarea 4: Crear Presentation Deck
**Tiempo:** 1 hora  
**Status:** No iniciado

```
SLIDES NECESARIOS (10 minutos de presentación):

1️⃣ Portada
   - Nombre del proyecto
   - Equipo de desarrollo
   - Fecha

2️⃣ El Problema
   - Agricultores necesitan gestionar cultivos
   - Distribuidores necesitan inventario
   - Técnicos necesitan sensores
   - TODO sin sistema unificado

3️⃣ La Solución
   - Backend profesional con Django REST
   - API moderna con JWT
   - Sistema de roles y permisos
   - BD en la nube

4️⃣ Arquitectura
   - 4 apps: core, cultivos, inventario, sensores
   - 5 roles: admin, agricultor, distribuidor, técnico, usuario
   - MySQL en Railway
   - Desplegado en Render

5️⃣ Funcionalidades Principales
   - Registro con rol
   - CRUD de cultivos
   - Control de inventario
   - Lectura de sensores
   - Logs de auditoría

6️⃣ Seguridad
   - Autenticación JWT
   - Permisos por rol
   - Validación de datos
   - HTTPS en producción

7️⃣ Demo (parte técnica)
   [GIF o video grabado mostrando:]
   - Swagger abierto
   - POST /api/auth/register/ (nuevo usuario)
   - POST /api/auth/login/ (obtener token)
   - GET /api/cultivos/ (listar cultivos)
   - POST /api/cultivos/ (crear cultivo)
   - GET /api/core/health/ (verificar estado)

8️⃣ Resultados
   - 35+ tests pasando
   - 0 errores de linting
   - API documentada
   - BD en producción
   - 95% cobertura de requisitos

9️⃣ Conclusión
   - Sistema profesional listo para producción
   - Escalable y mantenible
   - Seguro y confiable
   - Mejora la productividad agrícola

🔟 Q&A
   - Preguntas de los evaluadores
```

### Tarea 5: Preparar Demo Técnica
**Tiempo:** 1 hora  
**Status:** No iniciado

```
DEMO VIVA (si es posible):

1. Abrir Swagger en producción
   URL: https://agromanager-api.onrender.com/api/schema/swagger/

2. Mostrar endpoint de registro
   - Explicar que pide ROLE obligatorio
   - Mostrar validación de password
   - Mostrar validación de email

3. Crear usuario de prueba
   POST /api/auth/register/
   Rol: agricultor
   Password: CorrectPassword123!@#

4. Login con el usuario
   POST /api/auth/login/
   Mostrar JWT token recibido

5. Usar token para crear cultivo
   POST /api/cultivos/
   Header: Authorization: Bearer {token}
   Payload: nombre, tipo, variedad

6. Verificar que solo ve sus cultivos
   GET /api/cultivos/

7. Health check
   GET /api/core/health/
   Mostrar que BD está conectada

8. Logs (si hay tabla de auditoría)
   GET /api/core/audit/
   Mostrar que registra cada acción

ALTERNATIVA: Grabar GIF de 2 minutos con todo esto
```

---

## 📋 CHECKLIST FINAL (ANTES DE VIERNES 12)

### Código

```
□ Despliegue en Render completado y verificado
□ ManyToMany relaciones agregadas en 4 apps
□ Tests de Sensores mejorados (5+ tests)
□ Todos los tests pasando: python manage.py test
□ Migraciones aplicadas en producción
□ No hay WARNING en Django: python manage.py check --deploy
□ Swagger funciona en: https://agromanager-api.onrender.com/api/schema/swagger/
□ Health check responde 200: https://agromanager-api.onrender.com/api/core/health/
□ JWT login funciona
```

### Documentación

```
□ README.md actualizado con URL de Render
□ Explicación de roles clara
□ Guía de uso en Swagger
□ Variables de entorno documentadas
□ Instrucciones de despliegue en DESPLIEGUE_RENDER.md
□ Todos los endpoints documentados
□ Ejemplos de curl para cada endpoint
□ Troubleshooting guide incluido
```

### Presentación

```
□ Slides creadas (9 diapositivas)
□ Demo ensayada (2 minutos)
□ Q&A anticipadas
□ Tiempo total: 10 minutos
□ Presentador #1: introducción + arquitectura
□ Presentador #2: funcionalidades + seguridad
□ Presentador #3: demo técnica + conclusión
□ Backup: Video de 2 minutos grabado
```

### Git

```
□ Último commit: "Despliegue en Render - Proyecto completado"
□ Branch: prueva-antes-main
□ Tags: v1.0.0 (versión final)
□ No hay cambios sin commitear
□ README actualizado en GitHub
```

---

## ⏱️ TIMELINE RECOMENDADO

### Hoy (Miércoles 11 de diciembre, ~24:00)

```
22:00 → Leer este documento
22:15 → Asegurar que todo esté commiteado en GitHub
22:30 → Dormir (descanso importante)
```

### Mañana Temprano (Jueves 12 de diciembre)

```
08:00 → Desayuno y verificar todo en dev local
08:30 → DESPLIEGUE EN RENDER (45 min) - CRÍTICO
09:15 → Verificar salud en producción
09:30 → Agregar ManyToMany en apps (30 min)
10:00 → Mejorar tests de Sensores (30 min)
10:30 → Ejecutar suite de tests
11:00 → ALMUERZO
11:45 → Crear presentation deck
12:45 → Grabar/preparar demo técnica
13:45 → Ensayar presentación (10 min)
14:00 → Buffer para ajustes finales
15:00 → LISTO PARA EXPOSICIÓN
```

---

## 🚨 COSAS QUE NO OLVIDES

```
❌ NO cambiar README antes de desplegar en Render
✅ SI actualizar README con URL de Render después

❌ NO desplegar sin verificar health check local
✅ SI verificar primero: python manage.py runserver

❌ NO hacer push a main sin estar 100% seguro
✅ SI quedarse en prueva-antes-main hasta Friday

❌ NO introducir nuevas funcionalidades
✅ SI solo pulir lo existente

❌ NO modificar modelos sin migrations
✅ SI crear migration: python manage.py makemigrations

❌ NO cambiar SECRET_KEY entre env
✅ SI usar la misma en dev y prod (mejor: generar nueva para prod)

❌ NO exponer DATABASE_URL en GitHub
✅ SI usar .env y .env.example

❌ NO desplegar sin backup
✅ SI descargar migrations y modelos como backup

❌ NO olvidar collectstatic en release
✅ SI está en Procfile release command
```

---

## 💎 PUNTOS CLAVE PARA PRESENTACIÓN

```
1. Decir: "Sistema de roles obligatorio en registro"
   NO: "Sistema de roles opcional"

2. Decir: "Permisos granulares por rol y acción"
   NO: "Solo permisos de lectura/escritura"

3. Decir: "BD en producción con Railway, API en Render"
   NO: "Todo en Railway" o "Todo en Render"

4. Decir: "35+ tests garantizan calidad"
   NO: "Código sin tests"

5. Decir: "Documentación profesional (1000+ líneas)"
   NO: "README básico"

6. Decir: "Cumple 95% de requisitos del proyecto"
   NO: "Solo cumple lo mínimo"
```

---

## 📱 CONTACTOS DE EMERGENCIA

Si algo falla:

```
Render: https://render.com/account/login
Railway: https://railway.app/
GitHub: https://github.com/samuelcastr/AgroManager-ProyectoFinal

Documentación:
- DESPLIEGUE_RENDER.md (troubleshooting)
- ESTADO_FINAL.md (resumen completo)
- SISTEMA_ROLES_PERMISOS.md (arquitectura)
```

---

## 🎯 OBJETIVO FINAL

```
✅ SISTEMA PROFESIONAL
✅ DESPLEGADO EN PRODUCCIÓN
✅ DOCUMENTADO COMPLETAMENTE
✅ PRESENTACIÓN LISTA
✅ 95%+ CUMPLIMIENTO DE REQUISITOS
✅ LISTA PARA NOTA MÁXIMA
```

---

**Última Actualización:** 11 de diciembre de 2025, 23:45  
**Estado:** 🟢 Listo para proceder  
**Próximo Paso:** Despliegue en Render (máxima prioridad)  

¡VAMOS A TERMINAR ESTO EN GRANDE! 🚀
