from django.contrib import admin
from .models import Cultivo, CicloSiembra, Variedad


@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'tipo', 'unidad_productiva')


@admin.register(CicloSiembra)
class CicloAdmin(admin.ModelAdmin):
	list_display = ('cultivo', 'fecha_siembra', 'fecha_cosecha_estimada', 'estado')


@admin.register(Variedad)
class VariedadAdmin(admin.ModelAdmin):
	list_display = ('nombre',)
