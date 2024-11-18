from django.contrib import admin

from Apps.Catalogos.Paciente.models import Paciente


@admin.register(Paciente)
# Register your models here.
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['numero_cedula', 'nombres', 'apellidos', 'fecha_nacimiento', 'telefono', 'correo_electronico', 'direccion', 'activo', 'codigoPaciente', 'usuario']
    search_fields = ['nombres']