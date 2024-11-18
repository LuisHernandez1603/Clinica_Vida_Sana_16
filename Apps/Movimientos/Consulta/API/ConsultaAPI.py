from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from Apps.Movimientos.Cita.models import Cita
from Apps.Movimientos.Consulta.API.Serializer import ConsultaSerializer
from Apps.Movimientos.Consulta.models import Consulta
from Apps.Catalogos.Paciente.API.Permission import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from Apps.Utils.ResponseData import ResponseData

class ConsultaViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        consulta_activo = Consulta.objects.filter(activo=True)
        serializer = ConsultaSerializer(consulta_activo, many=True)
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
            Message="Listado de Consultas",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            serializer = ConsultaSerializer(Consulta.objects.get(pk=pk))
            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="Datos de la Consulta",
                Record=serializer.data  # Datos a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Consulta.DoesNotExist:
            # En el caso de que no exista el paciente, retornará un error
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Consulta no encontrada",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    @action(methods=['post'], detail=False)
    def ProgramarConsulta(self, request, pk=None):
        serializer = ConsultaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener la cita asociada a la consulta
        cita_id = serializer.validated_data.get('cita').id
        try:
            cita = Cita.objects.get(id=cita_id)
        except Cita.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="La Cita asociada no existe",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        # Verificar si la cita está activa
        if not cita.activo:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="No se puede registrar una Consulta para una Cita anulada",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        if Consulta.objects.filter(
                codigo_Consulta=serializer.validated_data[
                    'codigo_Consulta']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro de la Consulta ya existe con ese mismo código",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())
        serializer.save()
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_201_CREATED,  # Muestra el estado de la respuesta
            Message="Consulta registrada exitosamente",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())
        #serializer = ConsultaSerializer(data=request.data)
        #try:
            #serializer.is_valid(raise_exception=True)
            #serializer.save()
            #return Response(status=status.HTTP_200_OK, data=serializer.data)
        #except:
            #return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error al ingresar datos de la consulta'})

    def update(self, request, pk: int):
        try:
            consulta = Consulta.objects.get(pk=pk)
            serializer = ConsultaSerializer(instance=consulta, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="La información de la Consulta ha sido actualizada exitosamente",
                Record=serializer.data  # Datos actualizados a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Consulta.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Consulta no encontrada",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())
        except:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ha ocurrido un error al intentar actualizar la información de la Consulta",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

    def destroy(self, request, pk=None):
        # Se busca el objeto Consulta usando el pk
        try:
            consulta = Consulta.objects.get(pk=pk)
        except Consulta.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Consulta no encontrada",
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        # Verificar si el Consulta ya está inactivo
        if not consulta.activo:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="La Consulta ya está inactiva",
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Marcar al Consulta como inactiva
        consulta.activo = False
        consulta.save()

        # Retornar la respuesta de éxito
        data = ResponseData(
            Success=True,
            Status=status.HTTP_204_NO_CONTENT,
            Message="El registro de la Consulta está marcado como inactivo",
            Record=[]
        )
        return Response(status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

    #def destroy (self, request, pk: int):
        #try:
            #cita = Consulta.objects.get(pk=pk)
            #serializer = ConsultaSerializer(cita)
            #cita.delete()
            #return Response(status=status.HTTP_204_NO_CONTENT)
        #except Consulta.DoesNotExist:
            #return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'La consulta ya ha sido eliminada'})
