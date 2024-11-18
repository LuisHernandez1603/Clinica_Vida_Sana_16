from django.db import models
from Apps.Catalogos.Paciente.models import Paciente
from Apps.Catalogos.Recepcionista.models import Recepcionista
from Apps.Movimientos.Doctor.models import Doctor
# Create your models here.
class Cita(models.Model):
    confirmacion = models.BooleanField()
    fecha_hora = models.DateTimeField()
    paciente = models.ForeignKey(Paciente, on_delete= models.RESTRICT)
    doctor = models.ForeignKey(Doctor, on_delete=models.RESTRICT)
    recepcionista = models.ForeignKey(Recepcionista, on_delete=models.RESTRICT)
    codigoCita= models.CharField(max_length=5)
    activo = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

    def __str__(self):
        return self.codigoCita