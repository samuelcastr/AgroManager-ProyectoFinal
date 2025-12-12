from django.db import models


class Sensor(models.Model):
	TIPOS_SENSOR = [
		('HUMEDAD', 'Humedad'),
		('PH', 'pH'),
		('TEMPERATURA', 'Temperatura'),
	]
	serial = models.CharField(max_length=100, unique=True)
	tipo = models.CharField(max_length=20, choices=TIPOS_SENSOR)
	ubicacion = models.CharField(max_length=255, blank=True, null=True)
	creado = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.serial} ({self.tipo})"


class LecturaSensor(models.Model):
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='lecturas')
	timestamp = models.DateTimeField(db_index=True)
	valor = models.DecimalField(max_digits=10, decimal_places=3)
	raw_payload = models.JSONField(blank=True, null=True)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f"{self.sensor.serial} @ {self.timestamp}: {self.valor}"
