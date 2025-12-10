✅ EXPLICACIÓN DE LA RESPUESTA 400 EN SWAGGER

═══════════════════════════════════════════════════════════════════════════
¿QUÉ PASABA ANTES?
═══════════════════════════════════════════════════════════════════════════

Lo que viste en Swagger:
┌─────────────────────────────────────────────────────────────────┐
│ POST /api/auth/register/                                        │
│                                                                 │
│ Request Body: (Swagger enviaba VACÍO)                          │
│ -d ''                                                           │
│                                                                 │
│ Response: 400 Bad Request                                       │
│                                                                 │
│ {                                                              │
│   "username": ["Este campo es requerido."],                   │
│   "email": ["Este campo es requerido."],                      │
│   "password": ["Este campo es requerido."],                   │
│   "password2": ["Este campo es requerido."],                  │
│   "first_name": ["Este campo es requerido."],                 │
│   "last_name": ["Este campo es requerido."]                   │
│ }                                                              │
└─────────────────────────────────────────────────────────────────┘

¿POR QUÉ PASABA ESTO?

Razón 1: Swagger no mostraba campos
- Usaba @api_view decorator (limitado)
- drf-yasg no generaba esquema para los campos
- Swagger no sabía cómo mostrar las entradas

Razón 2: El body estaba vacío
- Sin campos visuales, Swagger enviaba -d ''
- La API validaba y retornaba 400
- Los campos aparecían como "requerido"

═══════════════════════════════════════════════════════════════════════════
¿QUÉ PASA AHORA?
═══════════════════════════════════════════════════════════════════════════

Ahora Swagger muestra:
┌─────────────────────────────────────────────────────────────────┐
│ POST /api/auth/register/                                        │
│                                                                 │
│ Try it out                                                      │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ REQUEST BODY                                                ││
│ ├─────────────────────────────────────────────────────────────┤│
│ │ username          [_________________________]                ││
│ │ Nombre de usuario único                                     ││
│ │                                                             ││
│ │ email             [_________________________]                ││
│ │ Email válido y único                                        ││
│ │                                                             ││
│ │ password          [_________________________]                ││
│ │ Mínimo 8 caracteres con mayúscula, minúscula y número      ││
│ │                                                             ││
│ │ password2         [_________________________]                ││
│ │ Debe coincidir exactamente con la contraseña anterior      ││
│ │                                                             ││
│ │ first_name        [_________________________]                ││
│ │ Tu nombre                                                   ││
│ │                                                             ││
│ │ last_name         [_________________________]                ││
│ │ Tu apellido                                                 ││
│ │                                                             ││
│ │                          [EXECUTE]                          ││
│ └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘

Cuando haces clic en "Execute":
┌─────────────────────────────────────────────────────────────────┐
│ Response                                                        │
│                                                                 │
│ Code: 201                                                       │
│ Created                                                         │
│                                                                 │
│ {                                                              │
│   "message": "Usuario registrado exitosamente",               │
│   "user": {                                                    │
│     "id": 5,                                                   │
│     "username": "testuser_final",                             │
│     "email": "testfinal@example.com",                         │
│     "first_name": "Test",                                     │
│     "last_name": "User"                                       │
│   }                                                            │
│ }                                                              │
└─────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
¿CÓMO SE SOLUCIONÓ?
═══════════════════════════════════════════════════════════════════════════

Cambio 1: RegisterSerializer (apps/core/serializers.py)
────────────────────────────────────────────────────────

ANTES:
password = serializers.CharField(write_only=True, required=True)

AHORA:
password = serializers.CharField(
    write_only=True,
    required=True,
    help_text='Mínimo 8 caracteres con mayúscula, minúscula y número'
)

→ help_text: Swagger ve las descripciones
→ style: Swagger sabe si es password, email, etc


Cambio 2: RegisterAPIView (apps/core/views.py)
───────────────────────────────────────────────

ANTES:
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def register(request):
    ...

AHORA:
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description='Crear nuevo usuario...',
        request_body=RegisterSerializer,
        responses={...}
    )
    def post(self, request):
        ...

→ APIView: Mejor soporte para Swagger
→ @swagger_auto_schema: Le dice a drf-yasg cómo generar el esquema
→ request_body=RegisterSerializer: Los campos vienen del serializer


Cambio 3: config/urls.py
────────────────────────

ANTES:
from views import register
path('api/auth/register/', register)

AHORA:
from views import RegisterAPIView
path('api/auth/register/', RegisterAPIView.as_view())

→ .as_view(): Convierte la clase en una vista que Django entiende

═══════════════════════════════════════════════════════════════════════════
¿POR QUÉ @api_view TENÍA PROBLEMAS?
═══════════════════════════════════════════════════════════════════════════

@api_view es un decorador para vistas funcionales:
✅ Rápido para casos simples
❌ Limitado para Swagger
❌ No detecta automáticamente campos
❌ No genera buenos esquemas

APIView es una clase que hereda de View:
✅ Más control
✅ Excelente soporte Swagger
✅ Detecta automáticamente campos del serializer
✅ Genera esquemas completos

═══════════════════════════════════════════════════════════════════════════
✅ RESULTADO FINAL
═══════════════════════════════════════════════════════════════════════════

Swagger ahora:
✅ Muestra campos visuales
✅ Cada campo tiene descripción (help_text)
✅ Se pueden completar los campos
✅ Se puede hacer "Execute" y registrarse
✅ Retorna 201 Created con los datos del usuario

Form-Data ahora:
✅ Funciona sin JSON
✅ Aceptado por el servidor
✅ Retorna 201 Created

JSON sigue funcionando:
✅ Como siempre
✅ Retorna 201 Created

═══════════════════════════════════════════════════════════════════════════

En resumen:
El error 400 que veías era porque Swagger enviaba un body vacío.
Ahora Swagger muestra los campos y envía los datos correctamente.
¡El problema está completamente resuelto! 🎉
