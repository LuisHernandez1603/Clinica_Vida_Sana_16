from rest_framework.serializers import ModelSerializer

from Apps.Catalogos.Especialidad.models import Especialidad


class EspecialidadSerializer(ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id','nombre', 'descripcion', 'codigo_interno', 'activo']