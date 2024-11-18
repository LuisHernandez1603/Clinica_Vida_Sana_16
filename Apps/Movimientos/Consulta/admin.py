from django.contrib import admin

from Apps.Movimientos.Consulta.models import Consulta


@admin.register(Consulta)
# Register your models here.
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['cita', 'descripcion', 'diagnostico', 'recomendaciones', 'codigo_Consulta', 'activo']
    search_fields = ['descripcion']