from rest_framework import serializers
from .models import ExportRequest

class ExportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportRequest
        fields = ['id', 'app', 'created_at']
        read_only_fields = ['id', 'created_at']
