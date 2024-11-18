from django.db import models

# Create your models here.
class Recepcionista(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=8)
    correo_electronico = models.CharField(max_length=100, null=True)
    fecha_ingreso = models.DateTimeField()
    codigoRecepcionista= models.CharField(max_length=5)
    activo = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

    def __str__(self):
        return self.nombre