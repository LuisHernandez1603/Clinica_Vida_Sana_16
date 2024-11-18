from rest_framework.serializers import ModelSerializer
from Apps.Catalogos.Paciente.API.Serializer import PacienteSerializer
from Apps.Catalogos.Recepcionista.API.Serializer import RecepcionistaSerializer
from Apps.Movimientos.Cita.models import Cita
from Apps.Movimientos.Doctor.API.Serializer import DoctorSerializer


#from Apps.Movimientos.Doctor.


class CitaSerializer(ModelSerializer):

    class Meta:
        model = Cita
        fields = ['id','confirmacion','fecha_hora', 'paciente', 'doctor', 'recepcionista', 'codigoCita', 'activo']
