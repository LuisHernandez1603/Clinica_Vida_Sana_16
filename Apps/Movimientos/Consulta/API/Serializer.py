from rest_framework.serializers import ModelSerializer

from Apps.Movimientos.Consulta.models import Consulta


class ConsultaSerializer(ModelSerializer):
    class Meta:
        model = Consulta
        fields = ['id','cita','descripcion', 'diagnostico', 'recomendaciones', 'codigo_Consulta', 'activo']