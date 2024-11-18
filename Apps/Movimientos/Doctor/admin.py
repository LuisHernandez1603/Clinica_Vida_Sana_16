from django.contrib import admin

from Apps.Movimientos.Doctor.models import Doctor


@admin.register(Doctor)
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'telefono', 'correo_electronico', 'especialidad', 'codigo_Doctor', 'activo']
    search_fields = ['nombre']