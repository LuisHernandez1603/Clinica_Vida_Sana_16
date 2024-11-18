from django.db import models
from Apps.Movimientos.Cita.models import Cita
# Create your models here.
class Consulta(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.RESTRICT)
    descripcion = models.CharField(max_length=100)
    diagnostico = models.TextField()
    recomendaciones = models.TextField()
    codigo_Consulta = models.CharField(max_length=5)
    activo = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

    def __str__(self):
        return self.diagnostico