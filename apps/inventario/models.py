from django.db import models
from django.db import transaction

class Insumo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    unidad_medida = models.CharField(max_length=20)  # ej: kg, litros, unidades
    stock_minimo = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

    @property
    def total_stock(self) -> int:
        """Retorna la suma de `cantidad_actual` de todos los lotes del insumo."""
        return sum(self.lotes.values_list("cantidad_actual", flat=True) or [])


class Lote(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name="lotes")
    cantidad_actual = models.PositiveIntegerField()
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Lote de {self.insumo.nombre} ({self.cantidad_actual})"


class MovimientoStock(models.Model):
    TIPO_CHOICES = [
        ("ENTRADA", "Entrada"),
        ("SALIDA", "Salida"),
        ("AJUSTE", "Ajuste"),
    ]

    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.insumo.nombre} ({self.cantidad})"


# 🔥 Operación atómica para salidas de stock
def registrar_salida_stock(insumo: Insumo, cantidad: int, descripcion: str = ""):
    from django.core.exceptions import ValidationError

    with transaction.atomic():

        # 1. Verificar cantidad total disponible
        total_disponible = insumo.total_stock
        if cantidad > total_disponible:
            raise ValidationError("No hay suficiente stock para realizar esta operación")

        # 2. Consumir del primer lote disponible (FIFO)
        cantidad_restante = cantidad
        lotes = insumo.lotes.order_by("fecha_ingreso")

        for lote in lotes:
            if lote.cantidad_actual >= cantidad_restante:
                lote.cantidad_actual -= cantidad_restante
                lote.save()
                cantidad_restante = 0
                break
            else:
                cantidad_restante -= lote.cantidad_actual
                lote.cantidad_actual = 0
                lote.save()

        # 3. Registrar movimiento
        MovimientoStock.objects.create(
            insumo=insumo,
            tipo="SALIDA",
            cantidad=cantidad,
            descripcion=descripcion,
        )

        return True
