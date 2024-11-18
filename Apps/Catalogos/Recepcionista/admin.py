from django.contrib import admin

from Apps.Catalogos.Recepcionista.models import Recepcionista


@admin.register(Recepcionista)
# Register your models here.
class RecepcionistaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos' ,'telefono', 'correo_electronico', 'fecha_ingreso', 'codigoRecepcionista', 'activo']
    search_fields = ['nombre']