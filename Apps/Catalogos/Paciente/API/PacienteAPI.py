from datetime import date
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from Apps.Catalogos.Paciente.API.Serializer import PacienteSerializer
from Apps.Catalogos.Paciente.models import Paciente
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action, permission_classes
from Seguridad.Usuario.API.PermissionsUser import IsAdminOrSelfPatient
#from Seguridad.Usuario.API.PermissionsUser import IsSuperuser
#from Seguridad.Usuario.API.PermissionsUser import IsOwnPatient
#from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from Apps.Catalogos.Paciente.API.Permission import IsAdminOrReadOnly
from Apps.Utils.ResponseData import ResponseData


class IsAdminOrSelfPatient(BasePermission):
    def has_permission(self, request, view):
        # Los administradores (superusuarios) pueden hacer cualquier acción (como GET, PUT, etc.)
        if request.user.is_superuser:
            return True
        # Si es paciente, puede crear o actualizar su propio registro
        if hasattr(request.user, 'role') and request.user.role == "paciente":
            if view.action in ['update', 'partial_update']:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        # Si el usuario es superusuario, puede acceder a cualquier objeto
        if request.user.is_superuser:
            return True
        # Si el usuario es un paciente, solo puede acceder a su propio objeto
        if hasattr(request.user, 'role') and request.user.role == "paciente":
            return obj.usuario.id == request.user.id
        return False

class PacienteViewSet(ViewSet):
    permission_classes = [IsAuthenticated]  # [IsAdminOrReadOnly]
    queryset = Paciente.objects.all()
    serializer = PacienteSerializer

    def get_queryset(self):
        """
        Si el usuario es administrador, retorna todos los pacientes.
        Si el usuario es paciente, retorna solo su propio registro.
        """
        if self.request.user.is_superuser:
            return Paciente.objects.all()
        return Paciente.objects.filter(usuario=self.request.user)

    def list(self, request):
        # Verificar si el usuario es un superusuario
        if not request.user.is_superuser:
            data = ResponseData(
                Success=False,  # Indica que el proceso no fue exitoso
                Status=status.HTTP_403_FORBIDDEN,  # Error 403 para denegar el acceso
                Message="No tiene permiso para acceder a esta lista",
                Record=[]
            )
            return Response(status=status.HTTP_403_FORBIDDEN, data=data.toResponse())
        # Filtrar solo los pacientes activos
        paciente_activo = Paciente.objects.filter(activo=True)
        serializer = PacienteSerializer(paciente_activo, many=True)
        data = ResponseData(
            Success=True, # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK, # Muestra el estado de la respuesta
            Message="Listado de Pacientes",
            Record=serializer.data # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            # Permitir acceso completo si el usuario es superusuario
            if request.user.is_superuser:
                paciente = Paciente.objects.get(pk=pk)

            # Si el usuario es paciente, verificar que solo acceda a su propio registro
            elif request.user.role == 'paciente':
                paciente = Paciente.objects.get(pk=pk)
                if paciente.usuario_id != request.user.id:
                    data = ResponseData(
                        Success=False,
                        Status=status.HTTP_403_FORBIDDEN,
                        Message="No tiene permiso para ver este registro",
                        Record=[]
                    )
                    return Response(status=status.HTTP_403_FORBIDDEN, data=data.toResponse())

            # Denegar acceso si el usuario no es superusuario ni paciente
            else:
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_403_FORBIDDEN,
                    Message="No tiene permiso para ver este registro",
                    Record=[]
                )
                return Response(status=status.HTTP_403_FORBIDDEN, data=data.toResponse())

            # Serializar y retornar el registro del paciente
            serializer = PacienteSerializer(paciente)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Datos del Paciente",
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Paciente.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Paciente no encontrado",
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = PacienteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Verificar si el paciente tiene el mismo código y si es en ese caso, entonces no se guardará
        if Paciente.objects.filter(
            codigoPaciente= serializer.validated_data[
                'codigoPaciente']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro del Paciente ya existe con ese mismo código",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())

        # Verificar si el paciente tiene el mismo numero_cedula y si es en ese caso, entonces no se guardará
        if Paciente.objects.filter(
                numero_cedula=serializer.validated_data[
                    'numero_cedula']).exists():
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_409_CONFLICT,
                Message="El registro del Paciente ya existe con esa misma cédula",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())

        # Verificar si el paciente tiene el mismo numero_cedula y si es en ese caso, entonces no se guardará
        if Paciente.objects.filter(
                    telefono=serializer.validated_data[
                        'telefono']).exists():
                data = ResponseData(
                    Success=False,  # Si el proceso no se ejecutó correctamente
                    Status=status.HTTP_409_CONFLICT,
                    Message="Ya existe un registro con el mismo número de teléfono",  # Mensaje para el usuario
                    Record=[]
                )
                return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())

        fecha_nacimiento = serializer.validated_data['fecha_nacimiento']
        diaActual = datetime.now().date()

        # Verificar si el paciente es menor de edad
        if diaActual.year - fecha_nacimiento.year < 18:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El paciente deber ser mayor de edad para registrarse",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # Verificación de permisos según el rol
        if request.user.is_superuser:
            # Si es superuser, permite registrar el paciente con los datos proporcionados
            serializer.save()
        elif request.user.role == 'paciente':
                # Si el usuario es un paciente, solo puede registrarse a sí mismo
            serializer.save(usuario=request.user)
        else:
                # Si no es superuser ni paciente, deniega el acceso
            data = ResponseData(
                    Success=False,
                    Status=status.HTTP_403_FORBIDDEN,
                    Message="No tienes permiso para registrar un paciente.",
                    Record=[]
            )
            return Response(status=status.HTTP_403_FORBIDDEN, data=data.toResponse())

            # Si se guarda exitosamente
        data = ResponseData(
                Success=True,
                Status=status.HTTP_201_CREATED,
                Message="Paciente registrado exitosamente",
                Record=serializer.data
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())



        # Mensaje de error detallado en caso de validación fallida
        #return Response(
           # {"detail": "Error al ingresar datos del paciente", "errors": serializer.errors},
            #status=status.HTTP_400_BAD_REQUEST
        #)

    def update(self, request, pk: int):
        try:
            # Buscar al paciente por pk
            paciente = Paciente.objects.get(pk=pk)

            # Si el usuario es superusuario, puede actualizar cualquier registro
            if request.user.is_superuser:
                # Serializar los datos del paciente y actualizarlos
                serializer = PacienteSerializer(paciente, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "Success": True,
                        "Status": status.HTTP_200_OK,
                        "Message": "Paciente actualizado exitosamente",
                        "Record": serializer.data
                    }, status=status.HTTP_200_OK)

            # Si el usuario es un paciente, verificar que solo pueda actualizar su propio registro
            elif request.user.role == 'paciente':
                print(f"Usuario autenticado ID: {request.user.id}")
                print(f"Paciente usuario_id: {paciente.usuario.id}")

                # Verificar si el id del usuario en el paciente coincide con el usuario autenticado
                if paciente.usuario.id == request.user.id:
                    # Excluir el campo 'usuario' de la solicitud de actualización
                    request_data = request.data.copy()
                    request_data.pop('usuario', None)  # Evita la actualización del campo 'usuario'

                    serializer = PacienteSerializer(paciente, data=request_data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({
                            "Success": True,
                            "Status": status.HTTP_200_OK,
                            "Message": "Tus datos han sido actualizados exitosamente.",
                            "Record": serializer.data
                        }, status=status.HTTP_200_OK)

                    # Si los datos no son válidos
                    return Response({
                        "Success": False,
                        "Status": status.HTTP_400_BAD_REQUEST,
                        "Message": "Datos no válidos.",
                        "Record": []
                    }, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({
                        "Success": False,
                        "Status": status.HTTP_403_FORBIDDEN,
                        "Message": "No tienes permiso para actualizar este registro.",
                        "Record": []
                    }, status=status.HTTP_403_FORBIDDEN)

            # Si el usuario no es un superusuario ni el paciente correspondiente
            else:
                return Response({
                    "Success": False,
                    "Status": status.HTTP_403_FORBIDDEN,
                    "Message": "No tienes permiso para actualizar este registro.",
                    "Record": []
                }, status=status.HTTP_403_FORBIDDEN)

        except Paciente.DoesNotExist:
            return Response({
                "Success": False,
                "Status": status.HTTP_404_NOT_FOUND,
                "Message": "Paciente no encontrado.",
                "Record": []
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "Success": False,
                "Status": status.HTTP_400_BAD_REQUEST,
                "Message": str(e),
                "Record": []
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Verificar si el usuario es administrador
        if not request.user.is_superuser:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_403_FORBIDDEN,
                Message="No tiene permisos para realizar esta acción",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_403_FORBIDDEN, data=data.toResponse())
        # Se busca el objeto Paciente usando el pk
        try:
            paciente = Paciente.objects.get(pk=pk)
        except Paciente.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message= "Paciente no encontrado",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        # Verificar si el paciente ya está inactivo
        if not paciente.activo:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El paciente ya está inactivo",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Marcar al paciente como inactivo
        paciente.activo = False
        paciente.save()

        # Retornar la respuesta de éxito
        data = ResponseData(
            Success=False,  # Si el proceso no se ejecutó correctamente
            Status=status.HTTP_204_NO_CONTENT,
            Message="Paciente marcado como inactivo",  # Mensaje para el usuario
            Record=[]
        )
        return Response(status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

    @action(methods=['post'], detail=False)
    def PostCalcularEdad(self, request, pk=int):
        # Verificar si el usuario autenticado es superuser
        if not request.user.is_superuser:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_403_FORBIDDEN,
                Message="No tienes permiso para realizar esta acción.",
                Record=[]
            )
            return Response(status=status.HTTP_403_FORBIDDEN, data=data.toResponse())
        #paciente_id = request.data.get('id')
        try:
            paciente_id = int(request.data.get('id', 0))
            paciente = Paciente.objects.get(id=paciente_id)
            fecha_nacimiento = paciente.fecha_nacimiento
            hoy = date.today()

            # Cálculo de la edad
            edad = hoy.year - fecha_nacimiento.year - (
                    (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
            )

            # Serializa el paciente y agrega el campo "edad"
            serializer = PacienteSerializer(paciente, many=False)
            paciente_data = serializer.data
            paciente_data['edad'] = edad  # Agregar el campo de edad

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Cálculo de edad exitoso",
                Record=paciente_data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Paciente.DoesNotExist:
            # Excepción en el caso de que el paciente no existe
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Paciente no encontrado.",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        except Exception:
            # Excepción general para otros errores
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                Message="Ocurrió un error inesperado",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data.toResponse())

    #@action(methods=['post'], detail=False)
    #def PostCalcularEdad(self, request, pk=int):
        #paciente_id = request.data.get('id')

        #try:
            #paciente = Paciente.objects.get(id=paciente_id)
            #fecha_nacimiento = paciente.fecha_nacimiento
           # hoy = date.today()

          #  if hoy.month > fecha_nacimiento.month or (
         #           hoy.month == fecha_nacimiento.month and hoy.day >= fecha_nacimiento.day):
        #        edad = hoy.year - fecha_nacimiento.year
       #     else:
      #          edad = hoy.year - fecha_nacimiento.year - 1

     #       serializer = PacienteSerializer(Paciente.objects.filter(paciente_id), many=True)
    #        data = ResponseData(
   #             Success=True, #Si el proceso se ejecutó correctamente
  #              Status=status.HTTP_200_OK,
#                Message="Se ha creado correctamente",
 #               Record=serializer.data #Datos que regresan al usuario

          #  )
         #   return Response(status=status.HTTP_200_OK, data=data.toResponse())

        #except Paciente.DoesNotExist:
            # Excepción en el caso de que el paciente no existe
            #data = ResponseData(
                #Success=False, #Si el proceso no se ejecutó correctamente
               # Status=status.HTTP_404_NOT_FOUND,
              #  Message="Paciente no encontrado.", # Mensaje para el usuario
             #   Record=[]
            #)
            #return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        #except Exception:
            # Excepción general para otros errores
            #data = ResponseData(
                #Success=False, #Si el proceso no se ejecutó correctamente
                #Status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                #Message="Ocurrió un error inesperado", # Mensaje para el usuario
                #Record=[]
            #)
            #return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data.toResponse())


            #return Response({
                #"Success": True,
                #"Message": "Cálculo de edad exitoso.",
                #"Status": status.HTTP_200_OK,
                #"Record": {
                    #"id": paciente.id,
                    #"edad": edad
                #}
            #}, status=status.HTTP_200_OK)

        #except Paciente.DoesNotExist:
            #return Response({
                #"Success": False,
                #"Message": "Paciente no encontrado.",
                #"Status": status.HTTP_404_NOT_FOUND,
                #"Record": {}
            #}, status=status.HTTP_404_NOT_FOUND)