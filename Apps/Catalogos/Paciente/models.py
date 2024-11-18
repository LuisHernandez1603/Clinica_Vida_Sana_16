from django.db import models

from Config import settings
from Seguridad.Usuario.models import Usuario


# Create your models here.
class Paciente(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numero_cedula = models.CharField(max_length=16, null= True, blank=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    fecha_nacimiento = models.DateTimeField()
    telefono = models.CharField(max_length=8)
    correo_electronico= models.CharField(max_length=100, null=True)
    direccion = models.CharField(max_length=100, null= True)
    activo = models.BooleanField(default=True)
    codigoPaciente= models.CharField(max_length=5)

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"