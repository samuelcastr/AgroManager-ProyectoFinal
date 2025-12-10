from django.contrib import admin

# Register your models here.

from .models import Sensor, LecturaSensor


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
	list_display = ('id', 'serial', 'tipo', 'ubicacion', 'creado')
	search_fields = ('serial', 'ubicacion')


@admin.register(LecturaSensor)
class LecturaSensorAdmin(admin.ModelAdmin):
	list_display = ('id', 'sensor', 'timestamp', 'valor')
	list_filter = ('sensor', 'timestamp')
	search_fields = ('sensor__serial',)
