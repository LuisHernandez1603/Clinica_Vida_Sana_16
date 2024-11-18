from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from Apps.Catalogos.Recepcionista.API.Serializer import RecepcionistaSerializer
from Apps.Catalogos.Recepcionista.models import Recepcionista
from Apps.Catalogos.Paciente.API.Permission import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from Apps.Utils.ResponseData import ResponseData


class RecepcionistaViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        # Sólo se filtran los registros activos
        recepcionista_activo = Recepcionista.objects.filter(activo=True)
        serializer = RecepcionistaSerializer(recepcionista_activo, many=True)
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
            Message="Listado de Recepcionista",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            serializer = RecepcionistaSerializer(Recepcionista.objects.get(pk=pk))
            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="Datos del Recepcionista",
                Record=serializer.data  # Datos a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Recepcionista.DoesNotExist:
            # En el caso de que no exista el Recepcionista, retornará un error
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Recepcionista no encontrado",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = RecepcionistaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Recepcionista.objects.filter(
                codigoRecepcionista=serializer.validated_data[
                    'codigoRecepcionista']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro del Recepcionista ya existe con ese mismo código",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())

        if Recepcionista.objects.filter(
                telefono=serializer.validated_data[
                    'telefono']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro del Recepcionista ya existe con ese mismo número de teléfono",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())

        if Recepcionista.objects.filter(
                correo_electronico=serializer.validated_data[
                    'correo_electronico']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro del Recepcionista ya existe con ese mismo correo electrónico",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())
        serializer.save()
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_201_CREATED,  # Muestra el estado de la respuesta
            Message="Recepcionista registrado exitosamente",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())
        #serializer = RecepcionistaSerializer(data=request.data)
        #try:
            #serializer.is_valid(raise_exception=True)
            #serializer.save()
            #return Response(status=status.HTTP_200_OK, data=serializer.data)
        #except:
            #return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error al ingresar datos del Recepcionista'})

    def update(self, request, pk: int):
        try:
            cita = Recepcionista.objects.get(pk=pk)
            serializer = RecepcionistaSerializer(instance=cita, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="La información del Recepcionista ha sido actualizada exitosamente",
                Record=serializer.data  # Datos actualizados a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Recepcionista.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El Recepcionista que intentas actualizar no existe",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())
        except:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ha ocurrido un error al intentar actualizar la información del Recepcionista", # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

    def destroy(self, request, pk=None):
        # Se busca el objeto Recepcionista usando el pk
        try:
            recepcionista = Recepcionista.objects.get(pk=pk)
        except Recepcionista.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Recepcionista no encontrado",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        # Verificar si el recepcionista ya está inactiva
        if not recepcionista.activo:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El Recepcionista ya está inactivo",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Marcar al especialidad como inactiva
        recepcionista.activo = False
        recepcionista.save()

        # Retornar la respuesta de éxito
        data = ResponseData(
            Success=False,  # Si el proceso no se ejecutó correctamente
            Status=status.HTTP_204_NO_CONTENT,
            Message="El registro del Recepcionista ha sido marcado como inactivo",  # Mensaje para el usuario
            Record=[]
        )
        return Response(status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

    #def delete (self, request, pk: int):
        #try:
            #cita = Recepcionista.objects.get(pk=pk)
            #serializer = RecepcionistaSerializer(cita)
            #cita.delete()
            #return Response(status=status.HTTP_204_NO_CONTENT)
        #except Recepcionista.DoesNotExist:
            #return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'El recepcionista ya ha sido eliminado'})
