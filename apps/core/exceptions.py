import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger('apps')


def custom_exception_handler(exc, context):
    """
    Exception handler personalizado que:
    - Captura todas las excepciones de Django REST Framework
    - Registra errores en logs
    - Retorna respuesta uniforme
    """
    response = exception_handler(exc, context)

    # Log del error
    logger.error(
        f"Error {getattr(response, 'status_code', 500)} en {context['view'].__class__.__name__}",
        exc_info=exc,
        extra={
            'request': context['request'],
            'view': context['view'].__class__.__name__,
        }
    )

    if response is not None:
        # Enriquecer la respuesta
        if 'detail' not in response.data:
            response.data = {
                'detail': str(response.data.get('detail', 'Error en la solicitud')),
                'code': getattr(response, 'status_code', 500),
                'errors': response.data if isinstance(response.data, dict) else {},
            }
    else:
        # Error no controlado
        logger.critical(f"Error no controlado: {exc}", exc_info=exc)
        response = Response(
            {
                'detail': 'Error interno del servidor',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'errors': {} if not hasattr(exc, '__dict__') else str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response


class APIException(Exception):
    """Excepción base personalizada para la API"""
    def __init__(self, detail, code=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.code = code or 'error'
        self.status_code = status_code
        super().__init__(self.detail)


class ValidationError(APIException):
    """Error de validación"""
    def __init__(self, detail, code='validation_error'):
        super().__init__(detail, code, status.HTTP_400_BAD_REQUEST)


class NotFoundError(APIException):
    """Recurso no encontrado"""
    def __init__(self, detail='Recurso no encontrado', code='not_found'):
        super().__init__(detail, code, status.HTTP_404_NOT_FOUND)


class PermissionDenied(APIException):
    """Permiso denegado"""
    def __init__(self, detail='Permiso denegado', code='permission_denied'):
        super().__init__(detail, code, status.HTTP_403_FORBIDDEN)


class Unauthorized(APIException):
    """No autenticado"""
    def __init__(self, detail='No autenticado', code='unauthorized'):
        super().__init__(detail, code, status.HTTP_401_UNAUTHORIZED)
