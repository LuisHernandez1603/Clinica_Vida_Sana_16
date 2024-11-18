from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from Apps.Catalogos.Especialidad.models import Especialidad
from Apps.Catalogos.Paciente.API.Permission import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny

from Apps.Catalogos.Paciente.models import Paciente
from Apps.Movimientos.Doctor.API.Serializer import DoctorSerializer
from Apps.Movimientos.Doctor.models import Doctor
from Apps.Utils.ResponseData import ResponseData


class DoctorViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        doctor_activo = Doctor.objects.filter(activo=True)
        serializer = DoctorSerializer(doctor_activo, many=True)
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
            Message="Listado de Doctores",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            serializer = DoctorSerializer(Doctor.objects.get(pk=pk))
            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="Datos del Doctor",
                Record=serializer.data  # Datos a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Doctor.DoesNotExist:
            # Excepción en el caso de que el doctor no existe
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Doctor no encontrado",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener la especialidad asociada al doctor
        especialidad_id = serializer.validated_data.get('especialidad').id

        try:
            especialidad = Especialidad.objects.get(id=especialidad_id)
        except Especialidad.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="La Especialidad asociada no existe",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        # Verificar si la especialidad está activa
        if not especialidad.activo:
            data = ResponseData(
                    Success=False,  # Si el proceso no se ejecutó correctamente
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message="No se puede registrar un Doctor para una Especialidad anulada",  # Mensaje para el usuario
                    Record=[]
                )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        if Doctor.objects.filter(
                codigo_Doctor=serializer.validated_data[
                    'codigo_Doctor']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro del Doctor ya existe con ese mismo código",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())

        if Doctor.objects.filter(
                telefono=serializer.validated_data[
                    'telefono']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro del Doctor ya existe con ese mismo número de teléfono",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())

        if Doctor.objects.filter(
                correo=serializer.validated_data[
                    'correo_electronico']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro del Doctor ya existe con ese mismo correo electrónico",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())
        serializer.save()
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_201_CREATED,  # Muestra el estado de la respuesta
            Message="El doctor ha sido registrado exitosamente",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())
        #serializer = DoctorSerializer(data=request.data)
        #try:

            #serializer.is_valid(raise_exception=True)
            #serializer.save()
            #return Response(status=status.HTTP_200_OK, data=serializer.data)
        #except:
            #return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Error al ingresar datos del doctor'})

    def update(self, request, pk: int):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(instance=doctor, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="La información del Doctor ha sido actualizada exitosamente",
                Record=serializer.data  # Datos actualizados a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Doctor.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Doctor no encontrado",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())
        except:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El registro del Doctor ya existe",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

    def destroy(self, request, pk=None):
        # Se busca el objeto Doctor usando el pk
        try:
            doctor = Doctor.objects.get(pk=pk)
            print("Doctor encontrado:", doctor)  # Depuración
        except Doctor.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Doctor no encontrado",
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        # Verificar si el Doctor ya está inactivo
        if not doctor.activo:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El Doctor ya está inactivo",
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Marcar al Doctor como inactivo
        doctor.activo = False
        doctor.save()
        data = ResponseData(
            Success=True,
            Status=status.HTTP_204_NO_CONTENT,
            Message="El registro del Doctor está marcado como inactivo",
            Record=[]
        )
        return Response(status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

    #def destroy (self, request, pk: int):
        #try:
            #doctor = Doctor.objects.get(pk=pk)
            #serializer = DoctorSerializer(doctor)
            #doctor.delete()
            #return Response(status=status.HTTP_204_NO_CONTENT)
        #except Doctor.DoesNotExist:
            #return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'El doctor ya ha sido eliminado'})


    @action(methods=['get'], detail=False)
    def GetDatosDoctor(self, request):
        # Verificar si el usuario es un paciente autenticado
        if request.user.is_authenticated:
            if request.user.is_superuser:
                # Si el usuario es superusuario, no hay restricción
                pass
            else:
                # Aquí, si el usuario no es superusuario, se verifica que sea paciente
                try:
                    paciente = Paciente.objects.get(usuario=request.user)
                except Paciente.DoesNotExist:
                    return Response({
                        "Success": False,
                        "Status": status.HTTP_404_NOT_FOUND,
                        "Message": "Paciente no encontrado.",
                        "Record": []
                    }, status=status.HTTP_404_NOT_FOUND)
        doctor= Doctor.objects.select_related('especialidad').all()

        #Serializar datos de doctores
        serializer= DoctorSerializer(doctor, many=True)
        #return Response(status=status.HTTP_200_OK, data=serializer.data)
        data = serializer.data

        for doctor_data in data:
            # Encuentra el doctor correspondiente en el queryset
            doctor_instance = doctor.get(id=doctor_data['id'])
            especialidad = doctor_instance.especialidad

            # Añadir la información de la especialidad al diccionario del doctor
            doctor_data['especialidad'] = {
                'id': especialidad.id,
                'nombre': especialidad.nombre,
                'descripcion': especialidad.descripcion
            }

        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
            Message="Información del doctor obtenida exitosamente",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())


