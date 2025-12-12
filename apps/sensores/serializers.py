from rest_framework import serializers
from .models import Sensor, LecturaSensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        extra_kwargs = {
            'serial': {'help_text': 'Numero de serie unico del sensor (ej: SENSOR-001)'},
            'tipo': {'help_text': 'Tipo de sensor. Opciones: HUMEDAD, PH, TEMPERATURA'},
            'ubicacion': {'help_text': 'Ubicacion fisica del sensor (ej: Parcela A, Invernadero Norte)'},
            'creado': {'help_text': 'Fecha de creacion (se genera automaticamente)'},
        }


class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturaSensor
        fields = '__all__'
        extra_kwargs = {
            'sensor': {'help_text': 'ID del sensor que realiza la lectura'},
            'valor': {'help_text': 'Valor medido (numero decimal con precision de 2 decimales)'},
            'timestamp': {'help_text': 'Fecha y hora de la lectura (se genera automaticamente)'},
            'es_valida': {'help_text': 'Indica si la lectura es valida (booleano, por defecto True)'},
        }
