from django.db import models
from django.conf import settings

class Variedad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    datos_agronomicos = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Cultivo(models.Model):
    TIPOS_CULTIVO = [
        ('cereal', 'Cereal'),
        ('leguminosa', 'Leguminosa'),
        ('frutal', 'Frutal'),
        ('hortaliza', 'Hortaliza'),
        ('forraje', 'Forraje'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPOS_CULTIVO)
    variedad = models.ForeignKey(
        Variedad, on_delete=models.SET_NULL, null=True, blank=True
    )
    unidad_productiva = models.CharField(max_length=100, blank=True, null=True)
    sensores = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class CicloSiembra(models.Model):
    EN_PROGRESO = 'EN_PROGRESO'
    FINALIZADO = 'FINALIZADO'
    ESTADO_CHOICES = [
        (EN_PROGRESO, 'En progreso'),
        (FINALIZADO, 'Finalizado'),
    ]

    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='ciclos')
    fecha_siembra = models.DateField()
    fecha_cosecha_estimada = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=EN_PROGRESO)

    superficie_hectareas = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    rendimiento_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cultivo.nombre} - {self.fecha_siembra}"
