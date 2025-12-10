from rest_framework import serializers
from django.db import transaction
from .models import Cultivo, CicloSiembra, Variedad
import json


class VariedadSerializer(serializers.ModelSerializer):
    datos_agronomicos = serializers.JSONField(
        required=False,
        allow_null=True,
        help_text='Datos agronomicos en formato JSON (ej: {"rendimiento": "8 ton/ha", "ciclo": "120 dias"})'
    )
    
    class Meta:
        model = Variedad
        fields = ['id', 'nombre', 'descripcion', 'datos_agronomicos']
        extra_kwargs = {
            'nombre': {
                'help_text': 'Nombre unico de la variedad (ej: Variedad A1)',
                'min_length': 2
            },
            'descripcion': {
                'help_text': 'Descripcion detallada de caracteristicas de la variedad',
                'required': False
            },
        }

    def validate_datos_agronomicos(self, value):
        """Validar que datos_agronomicos sea un diccionario JSON válido"""
        if value is None or value == '':
            return value
        
        if isinstance(value, str):
            try:
                json.loads(value)
            except json.JSONDecodeError as e:
                raise serializers.ValidationError(
                    f'Debe ser JSON válido. Error: {str(e)}. '
                    f'Ej: {{"rendimiento": "8 ton/ha", "ciclo": "120 dias"}}'
                )
        elif isinstance(value, dict):
            # Si es un diccionario, está bien
            pass
        else:
            raise serializers.ValidationError(
                'Debe ser JSON válido (diccionario). '
                'Ej: {"rendimiento": "8 ton/ha", "ciclo": "120 dias"}'
            )
        
        return value
    
    def validate_nombre(self, value):
        """Validar nombre de variedad"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError('El nombre debe tener mínimo 2 caracteres.')
        return value.strip()


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

    def create(self, validated_data):
        """Crear cultivo con variedad anidada"""
        variedad_data = validated_data.pop('variedad', None)
        
        # Crear cultivo
        cultivo = Cultivo.objects.create(**validated_data)
        
        # Crear variedad si se proporciona
        if variedad_data:
            variedad = Variedad.objects.create(**variedad_data)
            cultivo.variedad = variedad
            cultivo.save()
        
        return cultivo
    
    def to_representation(self, instance):
        """Personalizar la representación para incluir variedad"""
        data = super().to_representation(instance)
        # Si hay variedad, asegurar que se serializa correctamente
        if instance.variedad:
            data['variedad'] = VariedadSerializer(instance.variedad).data
        return data
