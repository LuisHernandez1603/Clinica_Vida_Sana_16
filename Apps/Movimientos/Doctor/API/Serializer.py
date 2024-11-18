from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from Apps.Catalogos.Especialidad.API.Serializer import EspecialidadSerializer
from Apps.Catalogos.Especialidad.models import Especialidad
from Apps.Movimientos.Doctor.models import Doctor


class DoctorSerializer(ModelSerializer):
    especialidad = PrimaryKeyRelatedField(queryset=Especialidad.objects.all()) # El PrimaryKeyRelatedField sirve para obtener el id de la Especialidad en vez de todo el objeto en el Json, el queryset busca una instancia existente de Especialidad
    class Meta:
        model = Doctor
        fields = ['id','nombre', 'apellidos', 'telefono', 'correo_electronico', 'especialidad', 'codigo_Doctor', 'activo']

