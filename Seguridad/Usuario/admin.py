from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Seguridad.Usuario.models import Usuario


@admin.register(Usuario)

# Register your models here.
class UsuarioAdmin(UserAdmin):
    pass