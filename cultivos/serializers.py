from rest_framework import serializers
from django.db import transaction
from django_filters import FilterSet, CharFilter, DateFromToRangeFilter, ChoiceFilter
import django_filters
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


class CultivoFilterSet(FilterSet):
    """
    FilterSet avanzado para Cultivo con búsquedas por:
    - nombre (case-insensitive)
    - tipo de cultivo
    - fecha de creación (rango)
    - categoría (variedad)
    """
    nombre = CharFilter(field_name='nombre', lookup_expr='icontains', label='Nombre del cultivo')
    tipo = CharFilter(field_name='tipo', lookup_expr='icontains', label='Tipo de cultivo')
    fecha_inicio = DateFromToRangeFilter(field_name='created_at', label='Rango de fecha de creación')
    variedad = CharFilter(field_name='variedad__nombre', lookup_expr='icontains', label='Nombre de variedad')
    unidad_productiva = CharFilter(field_name='unidad_productiva', lookup_expr='icontains', label='Unidad productiva')

    class Meta:
        model = Cultivo
        fields = ['nombre', 'tipo', 'fecha_inicio', 'variedad', 'unidad_productiva']


class CicloFilterSet(FilterSet):
    """
    FilterSet avanzado para CicloSiembra con búsquedas por:
    - nombre del cultivo (icontains)
    - estado (exacto)
    - rango de fechas de siembra
    - rango de fechas de cosecha
    """
    cultivo__nombre = CharFilter(field_name='cultivo__nombre', lookup_expr='icontains', label='Nombre del cultivo')
    estado = ChoiceFilter(field_name='estado', choices=CicloSiembra.ESTADO_CHOICES, label='Estado')
    fecha_siembra_inicio = django_filters.DateFilter(field_name='fecha_siembra', lookup_expr='gte', label='Fecha siembra desde')
    fecha_siembra_fin = django_filters.DateFilter(field_name='fecha_siembra', lookup_expr='lte', label='Fecha siembra hasta')
    fecha_cosecha_inicio = django_filters.DateFilter(field_name='fecha_cosecha_estimada', lookup_expr='gte', label='Fecha cosecha desde')
    fecha_cosecha_fin = django_filters.DateFilter(field_name='fecha_cosecha_estimada', lookup_expr='lte', label='Fecha cosecha hasta')

    class Meta:
        model = CicloSiembra
        fields = ['cultivo__nombre', 'estado', 'fecha_siembra_inicio', 'fecha_siembra_fin', 'fecha_cosecha_inicio', 'fecha_cosecha_fin']
