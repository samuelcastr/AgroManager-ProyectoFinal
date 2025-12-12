"""
Manejador global de excepciones para la API REST
Captura y procesa errores HTTP estándar (400, 401, 403, 404, 405, 500)
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Manejador personalizado de excepciones que captura y formatea errores
    de manera profesional.
    """
    # Llamar al manejador por defecto de DRF
    response = exception_handler(exc, context)

    # Si DRF maneja la excepción
    if response is not None:
        # Registrar el error
        logger.error(f"Error: {exc.__class__.__name__} - {str(exc)}", extra={
            'status_code': response.status_code,
            'request_method': context.get('request').method,
            'request_path': context.get('request').path,
        })

        # Formatear respuesta de error
        error_response = {
            'success': False,
            'status_code': response.status_code,
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
            }
        }

        # Agregar detalles adicionales si están disponibles
        if isinstance(response.data, dict):
            error_response['error']['details'] = response.data

        response.data = error_response
        return response

    # Manejar excepciones no capturadas por DRF
    logger.error(f"Error no manejado: {exc.__class__.__name__} - {str(exc)}", extra={
        'request_method': context.get('request').method,
        'request_path': context.get('request').path,
    })

    return Response({
        'success': False,
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'error': {
            'type': exc.__class__.__name__,
            'message': 'Error interno del servidor. Por favor intente más tarde.',
        }
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ErrorHandlerMiddleware:
    """
    Middleware para capturar errores que no sean manejados por la aplicación
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Error no capturado en middleware: {str(e)}", exc_info=True)
            return JsonResponse({
                'success': False,
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error': {
                    'type': e.__class__.__name__,
                    'message': 'Error interno del servidor. Por favor intente más tarde.',
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
