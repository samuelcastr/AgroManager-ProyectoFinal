from rest_framework import serializers
from .models import Insumo, Lote, MovimientoStock


class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ("id", "nombre", "unidad_medida", "stock_minimo")
        extra_kwargs = {
            'nombre': {'help_text': 'Nombre unico del insumo (ej: Fertilizante NPK 10-10-10)'},
            'unidad_medida': {'help_text': 'Unidad de medida (ej: kg, litros, unidades, gramos)'},
            'stock_minimo': {'help_text': 'Cantidad minima de stock antes de generar alerta (numero entero)'},
        }


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ("id", "insumo", "cantidad_actual", "fecha_ingreso")
        extra_kwargs = {
            'insumo': {'help_text': 'ID del insumo asociado'},
            'cantidad_actual': {'help_text': 'Cantidad actual disponible en el lote (numero entero positivo)'},
            'fecha_ingreso': {'help_text': 'Fecha de ingreso (se genera automaticamente)'},
        }


class MovimientoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoStock
        fields = ("id", "insumo", "tipo", "cantidad", "fecha", "descripcion")
        extra_kwargs = {
            'insumo': {'help_text': 'ID del insumo asociado'},
            'tipo': {'help_text': 'Tipo de movimiento: ENTRADA (ingreso), SALIDA (egreso), AJUSTE (ajuste de inventario)'},
            'cantidad': {'help_text': 'Cantidad del movimiento (numero entero positivo)'},
            'fecha': {'help_text': 'Fecha del movimiento (se genera automaticamente)'},
            'descripcion': {'help_text': 'Descripcion opcional del motivo del movimiento'},
        }


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
    insumo_id = serializers.IntegerField(help_text='ID del insumo a ajustar')
    tipo = serializers.ChoiceField(
        choices=["ENTRADA", "SALIDA", "AJUSTE"],
        help_text='Tipo de ajuste: ENTRADA (nuevo ingreso), SALIDA (extraccion), AJUSTE (correccion de inventario)'
    )
    cantidad = serializers.IntegerField(help_text='Cantidad a ajustar (numero entero positivo)')
    descripcion = serializers.CharField(
        allow_blank=True,
        required=False,
        help_text='Razon o descripcion del ajuste (opcional)'
    )


class AjusteMasivoSerializer(serializers.Serializer):
    items = AjusteItemSerializer(
        many=True,
        help_text='Array de items de ajuste. Cada item debe incluir insumo_id, tipo, cantidad y descripcion opcional.'
    )
