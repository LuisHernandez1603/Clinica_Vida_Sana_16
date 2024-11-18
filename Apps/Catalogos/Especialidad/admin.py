from django.contrib import admin

from Apps.Catalogos.Especialidad.models import Especialidad


@admin.register(Especialidad)
# Register your models here.
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'codigo_interno']
    search_fields = ['codigo_interno', 'nombre']