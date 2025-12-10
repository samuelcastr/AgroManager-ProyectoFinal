from rest_framework import serializers
from django.db import transaction
from .models import Cultivo, CicloSiembra, Variedad


class VariedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variedad
        fields = ['id', 'nombre', 'descripcion', 'datos_agronomicos']
        extra_kwargs = {
            'nombre': {'help_text': 'Nombre unico de la variedad (ej: Variedad A1)'},
            'descripcion': {'help_text': 'Descripcion detallada de caracteristicas de la variedad'},
            'datos_agronomicos': {'help_text': 'Datos agronomicos en JSON (rendimiento esperado, ciclo, etc)'},
        }


class CicloSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloSiembra
        fields = '__all__'
        extra_kwargs = {
            'cultivo': {'help_text': 'ID del cultivo asociado'},
            'fecha_siembra': {'help_text': 'Fecha de siembra en formato YYYY-MM-DD'},
            'fecha_cosecha_estimada': {'help_text': 'Fecha estimada de cosecha en formato YYYY-MM-DD'},
            'estado': {'help_text': 'Estado del ciclo: EN_PROGRESO, COMPLETADO, CANCELADO'},
        }

    def validate(self, data):
        fecha_siembra = data.get('fecha_siembra')
        fecha_cosecha = data.get('fecha_cosecha_estimada')
        if fecha_siembra and fecha_cosecha and fecha_siembra >= fecha_cosecha:
            raise serializers.ValidationError('`fecha_siembra` debe ser anterior a `fecha_cosecha_estimada`.')
        return data


class CultivoSerializer(serializers.ModelSerializer):
    ciclos = CicloSerializer(many=True, read_only=True)
    variedad = VariedadSerializer(required=False, allow_null=True)

    class Meta:
        model = Cultivo
        fields = ['id', 'nombre', 'tipo', 'variedad', 'unidad_productiva', 'sensores', 'ciclos', 'created_at', 'updated_at']
        extra_kwargs = {
            'nombre': {'help_text': 'Nombre descriptivo del cultivo (ej: Maiz Sur A)'},
            'tipo': {'help_text': 'Tipo de cultivo. Opciones: cereal, leguminosa, frutal, hortaliza, forraje'},
            'unidad_productiva': {'help_text': 'Ubicacion o identificador de la unidad productiva (opcional)'},
            'sensores': {'help_text': 'JSON con configuracion de sensores asociados (opcional)'},
        }
