from rest_framework import serializers
from django.db import transaction
from .models import Cultivo, CicloSiembra, Variedad


class VariedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variedad
        fields = ['id', 'nombre', 'descripcion', 'datos_agronomicos']


class CicloSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloSiembra
        fields = '__all__'

    def validate(self, data):
        fecha_siembra = data.get('fecha_siembra')
        fecha_cosecha = data.get('fecha_cosecha_estimada')
        if fecha_siembra and fecha_cosecha and fecha_siembra >= fecha_cosecha:
            raise serializers.ValidationError('`fecha_siembra` debe ser anterior a `fecha_cosecha_estimada`.')
        return data

    def create(self, validated_data):

        with transaction.atomic():
            ciclo = super().create(validated_data)
        
            return ciclo


class CultivoSerializer(serializers.ModelSerializer):
    ciclos = CicloSerializer(many=True, read_only=True)
    variedad = VariedadSerializer(required=False, allow_null=True)

    class Meta:
        model = Cultivo
        fields = ['id', 'nombre', 'tipo', 'variedad', 'unidad_productiva', 'sensores', 'ciclos', 'created_at', 'updated_at']
