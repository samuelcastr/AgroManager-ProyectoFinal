from rest_framework import serializers
from .models import Sensor, LecturaSensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturaSensor
        fields = '__all__'
