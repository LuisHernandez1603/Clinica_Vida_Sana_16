from django.db import models

# Create your models here.
class Especialidad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    codigo_interno = models.CharField(max_length=5)
    activo = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

    def __str__(self):
        return self.codigo_interno