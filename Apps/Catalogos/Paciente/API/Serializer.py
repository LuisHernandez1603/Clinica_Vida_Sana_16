from rest_framework.serializers import ModelSerializer, Serializer
from Apps.Catalogos.Paciente.models import Paciente


class PacienteSerializer(ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id','numero_cedula','nombres', 'apellidos', 'fecha_nacimiento', 'telefono', 'correo_electronico', 'direccion', 'codigoPaciente', 'activo', 'usuario']

    def create(self, validated_data):
        # Asignar el usuario autenticado al paciente al crear un nuevo registro
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


