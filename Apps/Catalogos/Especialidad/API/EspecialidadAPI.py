from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from Apps.Catalogos.Especialidad.API.Serializer import EspecialidadSerializer
from Apps.Catalogos.Especialidad.models import Especialidad
from Apps.Utils.ResponseData import ResponseData


class EspecialidadViewSet(ViewSet):
    permission_classes = [IsAuthenticated]  # [IsAdminOrReadOnly]
    queryset = Especialidad.objects.all()
    serializer = EspecialidadSerializer

    def list(self, request):
        especialidad_activo = Especialidad.objects.filter(activo=True)
        serializer = EspecialidadSerializer(especialidad_activo, many=True)
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
            Message="Listado de Especialidades",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            serializer = EspecialidadSerializer(Especialidad.objects.get(pk=pk))
            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="Datos de la Especialidad",
                Record=serializer.data  # Datos a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Especialidad.DoesNotExist:
            # En el caso de que no exista el paciente, retornará un error
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Especialidad no encontrada",  # Mensaje para el usuario
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = EspecialidadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Especialidad.objects.filter(
                codigo_interno=serializer.validated_data[
                    'codigo_interno']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro de la Especialidad ya existe con ese mismo código",  # Mensaje para el usuario
                Record=None
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())

        # Verificar si la especialidad tiene el mismo nombre y si es así, entonces retornará error
        if Especialidad.objects.filter(
                nombre=serializer.validated_data[
                    'nombre']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro del Paciente ya existe con ese mismo nombre",  # Mensaje para el usuario
                Record=None
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())
            # Verificar si la especialidad tiene la misma descripción y si es así, entonces retornará error
        if Especialidad.objects.filter(
                descripcion=serializer.validated_data[
                        'descripcion']).exists():
                data = ResponseData(
                    Success=False,  # Si el proceso no se ejecutó correctamente
                    Status=status.HTTP_409_CONFLICT,
                    Message="El registro de la Especialidad ya existe con esa misma descripcion",  # Mensaje para el usuario
                    Record=None
                )
                return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())
        serializer.save()
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_201_CREATED,  # Muestra el estado de la respuesta
            Message="Especialidad registrada exitosamente",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())
        #serializer = EspecialidadSerializer(data=request.data)
        #try:

            #serializer.is_valid(raise_exception=True)
            #serializer.save()
            #return Response(status=status.HTTP_200_OK, data=serializer.data)
        #except Exception as e:
            #return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

    def update(self, request, pk: int):
        try:
            especialidad = Especialidad.objects.get(pk=pk)
            serializer = EspecialidadSerializer(instance=especialidad, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="La información de la Especialidad ha sido actualizada exitosamente",
                Record=serializer.data  # Datos a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Especialidad.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="La Especialidad que intentas actualizar no existe",  # Mensaje para el usuario
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())#Ha ocurrido un error al intentar actualizar la especialidad
        except:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ha ocurrido un error al intentar actualizar la información de la Especialidad", # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

    def destroy(self, request, pk=None):
        try:
            especialidad = Especialidad.objects.get(pk=pk)
        except Especialidad.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message= "Especialidad no encontrada",  # Mensaje para el usuario
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        # Verificar si el paciente ya está inactivo
        if not especialidad.activo:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="La Especialidad ya está inactiva",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Marcar al paciente como inactivo
        especialidad.activo = False
        especialidad.save()

        # Retornar la respuesta de éxito
        data = ResponseData(
            Success=False,  # Si el proceso no se ejecutó correctamente
            Status=status.HTTP_204_NO_CONTENT,
            Message="Especialidad marcada como inactiva",  # Mensaje para el usuario
            Record=[]
        )
        return Response(status=status.HTTP_204_NO_CONTENT, data=data.toResponse())
        # Se busca el objeto Especialidad usando el pk
        #try:
            #especialidad = Especialidad.objects.get(pk=pk)
        #except Especialidad.DoesNotExist:
            #return Response({"detail": "Especialidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el especialidad ya está inactiva
        #if not especialidad.activo:
            #return Response({"detail": "La Especialidad ya está inactiva"}, status=status.HTTP_400_BAD_REQUEST)

        # Marcar al especialidad como inactiva
        #especialidad.activo = False
        #especialidad.save()

        # Retornar la respuesta de éxito
        #return Response({"detail": "Especialidad marcada como inactiva"}, status=status.HTTP_204_NO_CONTENT)
