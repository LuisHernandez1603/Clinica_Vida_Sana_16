from rest_framework.serializers import ModelSerializer
from Apps.Catalogos.Recepcionista.models import Recepcionista


class RecepcionistaSerializer(ModelSerializer):
    class Meta:
        model = Recepcionista
        fields = ['id','nombre','apellidos', 'telefono', 'correo_electronico', 'fecha_ingreso', 'codigoRecepcionista', 'activo']
