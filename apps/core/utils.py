import logging
from django.db import transaction
from functools import wraps
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import decorator_from_middleware_with_args
from rest_framework.response import Response
from rest_framework import status
import csv
from io import StringIO

logger = logging.getLogger('apps')


def atomic_transaction(func):
    """
    Decorador que envuelve una función en una transacción atómica.
    Si falla, hace rollback automático.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with transaction.atomic():
                return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Transacción fallida en {func.__name__}: {str(e)}", exc_info=e)
            raise
    return wrapper


def get_client_ip(request):
    """Obtener IP del cliente desde request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """Obtener User Agent del request"""
    return request.META.get('HTTP_USER_AGENT', '')


def send_email_async(subject, message, recipient_list, from_email=None):
    """
    Enviar email de forma asíncrona (opcional: usar Celery en producción)
    
    Args:
        subject (str): Asunto del email
        message (str): Cuerpo del email
        recipient_list (list): Lista de correos destinatarios
        from_email (str): Email remitente (por defecto del settings)
    """
    if not from_email:
        from_email = settings.EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email enviado exitosamente a {recipient_list}")
        return True
    except Exception as e:
        logger.error(f"Error enviando email: {str(e)}", exc_info=e)
        return False


def export_to_csv(queryset, fields):
    """
    Exportar queryset a CSV
    
    Args:
        queryset (QuerySet): Queryset a exportar
        fields (list): Lista de campos a incluir
        
    Returns:
        str: CSV como string
    """
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    
    for obj in queryset:
        row = {}
        for field in fields:
            value = getattr(obj, field, '')
            if hasattr(value, '__call__'):
                value = value()
            row[field] = value
        writer.writerow(row)
    
    return output.getvalue()


def standardize_response(data=None, message=None, code=None, status_code=status.HTTP_200_OK):
    """
    Estandarizar respuesta de API
    
    Args:
        data (dict): Datos a retornar
        message (str): Mensaje descriptivo
        code (str): Código de error/éxito personalizado
        status_code (int): HTTP status code
        
    Returns:
        Response: Respuesta DRF estandarizada
    """
    response_data = {
        'success': 200 <= status_code < 300,
        'code': code or str(status_code),
        'message': message or 'Operación exitosa',
        'data': data or {},
    }
    return Response(response_data, status=status_code)


def paginate_queryset(queryset, page=1, page_size=20):
    """
    Paginar queryset manualmente
    
    Args:
        queryset (QuerySet): Queryset a paginar
        page (int): Número de página (1-indexed)
        page_size (int): Cantidad de items por página
        
    Returns:
        tuple: (items, total, total_pages)
    """
    page = max(1, int(page))
    page_size = min(100, max(1, int(page_size)))
    
    total = queryset.count()
    total_pages = (total + page_size - 1) // page_size
    
    start = (page - 1) * page_size
    end = start + page_size
    
    items = queryset[start:end]
    
    return items, total, total_pages


class DictToObject:
    """Convertir diccionario a objeto con atributos"""
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    def __repr__(self):
        return str(self.__dict__)


def validate_date_range(start_date, end_date):
    """
    Validar rango de fechas
    
    Args:
        start_date (datetime): Fecha de inicio
        end_date (datetime): Fecha de fin
        
    Returns:
        bool: True si es válido
        
    Raises:
        ValueError: Si las fechas son inválidas
    """
    if start_date > end_date:
        raise ValueError("La fecha de inicio no puede ser mayor a la fecha de fin")
    return True


def get_date_range_filters(start_date_str=None, end_date_str=None, date_field='created_at'):
    """
    Construir filters para rango de fechas
    
    Args:
        start_date_str (str): Fecha inicio en formato YYYY-MM-DD
        end_date_str (str): Fecha fin en formato YYYY-MM-DD
        date_field (str): Nombre del campo de fecha en el modelo
        
    Returns:
        dict: Diccionario con filters
    """
    from datetime import datetime
    
    filters = {}
    
    if start_date_str:
        try:
            filters[f'{date_field}__gte'] = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if end_date_str:
        try:
            filters[f'{date_field}__lte'] = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    return filters
