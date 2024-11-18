from django.contrib import admin

from Apps.Movimientos.Cita.models import Cita


@admin.register(Cita)
# Register your models here.
class CitaAdmin(admin.ModelAdmin):
    list_display = ['confirmacion', 'fecha_hora', 'paciente', 'doctor', 'recepcionista', 'codigoCita', 'activo']
    search_fields = ['confirmacion']