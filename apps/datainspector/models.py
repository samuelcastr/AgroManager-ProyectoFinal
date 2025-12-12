from django.db import models

# No models necesarios para los endpoints de exportación de Excel

class ExportRequest(models.Model):
    APP_CHOICES = [
        ('cultivos', 'Cultivos'),
        ('inventario', 'Inventario'),
        ('sensores', 'Sensores')
    ]
    app = models.CharField(max_length=30, choices=APP_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exportación de {self.app} ({self.created_at})"
