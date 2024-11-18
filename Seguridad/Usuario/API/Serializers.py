from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from Seguridad.Usuario.models import Usuario

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    # Validar que ambas contraseñas coincidan
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    # Crear el usuario
    def create(self, validated_data):
        usuario = Usuario(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            #role=validated_data.get('role', 'paciente')
        )
        usuario.set_password(validated_data['password'])  # Encriptar la contraseña
        usuario.save()
        return usuario