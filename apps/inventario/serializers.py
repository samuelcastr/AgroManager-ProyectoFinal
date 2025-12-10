from rest_framework import serializers
from .models import Insumo, Lote, MovimientoStock


class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ("id", "nombre", "unidad_medida", "stock_minimo")


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ("id", "insumo", "cantidad_actual", "fecha_ingreso")


class InsumoAlertSerializer(serializers.ModelSerializer):
    total_stock = serializers.IntegerField()
    por_debajo = serializers.BooleanField()

    class Meta:
        model = Insumo
        fields = ("id", "nombre", "unidad_medida", "stock_minimo", "total_stock", "por_debajo")


class MovimientoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoStock
        fields = ("id", "insumo", "tipo", "cantidad", "fecha", "descripcion")


class AjusteItemSerializer(serializers.Serializer):
    insumo_id = serializers.IntegerField()
    tipo = serializers.ChoiceField(choices=["ENTRADA", "SALIDA", "AJUSTE"])  # AJUSTE will be treated as generic
    cantidad = serializers.IntegerField()
    descripcion = serializers.CharField(allow_blank=True, required=False)


class AjusteMasivoSerializer(serializers.Serializer):
    items = AjusteItemSerializer(many=True)
