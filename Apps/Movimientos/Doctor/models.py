from django.db import models
from Apps.Catalogos.Especialidad.models import Especialidad

# Create your models here.
class Doctor(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=8)
    correo_electronico = models.CharField(max_length=100)
    especialidad =models.ForeignKey(Especialidad, on_delete=models.RESTRICT)
    codigo_Doctor= models.CharField(max_length=5)
    activo = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

    def __str__(self):
        return self.nombre