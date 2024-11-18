from datetime import datetime, timedelta
from dateutil import parser
from rest_framework import status
from rest_framework.response import Response
from Apps.Catalogos.Paciente.models import Paciente
from Apps.Catalogos.Recepcionista.models import Recepcionista
from Apps.Movimientos.Cita.API.Serializer import CitaSerializer
from Apps.Movimientos.Cita.models import Cita
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from Apps.Catalogos.Paciente.API.Permission import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from Seguridad.Usuario.API.PermissionsUser import IsPacienteOrSuperuser
from Apps.Movimientos.Doctor.models import Doctor
from Apps.Utils.ResponseData import ResponseData


class CitaViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        cita_activo = Cita.objects.filter(activo=True)
        serializer = CitaSerializer(cita_activo, many=True)
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
            Message="Listado de Citas",
            Record=serializer.data  # Datos a regresar al usuario
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            # Intentar obtener la cita por el ID
            serializer = CitaSerializer(Cita.objects.get(pk=pk))
            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="Datos de la Cita",
                Record=serializer.data  # Datos a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Cita.DoesNotExist:
            # Si no existe la cita, retornará error
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Cita no encontrada",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())


    def update(self, request, pk: int):
        try:
            # Intentar obtener la cita por el ID
            cita = Cita.objects.get(pk=pk)
            # Serializar los datos y validar el formato
            serializer = CitaSerializer(instance=cita, data=request.data)
            serializer.is_valid(raise_exception=True)
            # Guardar la actualización
            serializer.save()
            data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
            Message="La información de la cita ha sido actualizada exitosamente",
            Record=serializer.data  # Datos actualizados a regresar al usuario
          )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        except Cita.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="La Cita que intentas actualizar no existe",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        except:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ha ocurrido un error al intentar actualizar la información de la Cita",  # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        #cita = Cita.objects.get(pk=pk)
        #serializer = CitaSerializer(instance=cita, data=request.data)
        #serializer.is_valid(raise_exception=True)
        #serializer.save()
        #return Response(status=status.HTTP_200_OK, data=serializer.data)

    def destroy(self, request, pk=None):
        # Se busca el objeto Cita usando el pk
        try:
            cita = Cita.objects.get(pk=pk)
        except Cita.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Cita no encontrada",
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        # Verificar si el Cita ya está inactivo
        if not Cita.activo:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="La Cita ya está inactiva",
                Record=[]
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Marcar la Cita como inactiva
        cita.activo = False
        cita.save()

        # Retornar la respuesta de éxito
        data = ResponseData(
            Success=True,
            Status=status.HTTP_204_NO_CONTENT,
            Message="El registro de la Cita está marcado como inactivo",
            Record=[]
        )
        return Response(status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

    #def destroy (self, request, pk: int):
        #try:
            # Intentar obtener la cita por el ID
            #cita = Cita.objects.get(pk=pk)
        #except Cita.DoesNotExist:
            # Si no existe, retornar un error 404
            #return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Cita no encontrada'})
        #Se borra la cita
        #cita.delete()
        #return Response(status=status.HTTP_204_NO_CONTENT)

        #cita = Cita.objects.get(pk=pk)
        #serializer = CitaSerializer(cita)
        #cita.delete()
        #return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def GetDatosCita(self, request):
        cita= Cita.objects.select_related('paciente', 'doctor', 'recepcionista').all()

        #Serializar datos de las citas
        serializer= CitaSerializer(cita, many=True)
        data = serializer.data
        for cita_data in data:
            # Encuentra la instancia de la cita correspondiente en el queryset
            cita_instance = cita.get(id=cita_data['id'])

            # Obtener y añadir la información del paciente, doctor y recepcionista
            if cita_instance.paciente:
                cita_data['paciente'] = {
                    'id': cita_instance.paciente.id,
                    'nombres': cita_instance.paciente.nombres,
                    'apellidos': cita_instance.paciente.apellidos,
                    # Añade aquí otros campos del paciente que quieras incluir
                }

            if cita_instance.doctor:
                cita_data['doctor'] = {
                    'id': cita_instance.doctor.id,
                    'nombre': cita_instance.doctor.nombre,
                    'apellidos': cita_instance.doctor.apellidos,
                    # Añade aquí otros campos del doctor que quieras incluir
                }

            if cita_instance.recepcionista:
                cita_data['recepcionista'] = {
                    'id': cita_instance.recepcionista.id,
                    'nombre': cita_instance.recepcionista.nombre,
                    'apellidos': cita_instance.recepcionista.apellidos,
                    # Añade aquí otros campos del recepcionista que quieras incluir
                }

            # Crear la estructura de respuesta usando ResponseData
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
            Message="Datos de la Cita obtenidos exitosamente",
            Record=serializer.data  # Datos actualizados a regresar al usuario
        )

        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    @action( methods=['get'], detail=False)
    def GetContarCitas(self, request):
        cantidadCitas = Cita.objects.count()
        data = ResponseData(
            Success=True,  # Indica que el proceso fue exitoso
            Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
            Message="Cantidad de Citas obtenidas exitosamente",
            Record={"cantidadCitas": cantidadCitas}  # Datos actualizados a regresar al usuario
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    @action(methods=['get'], detail=False)
    def GetOrdenCitasbyFecha(self, request):
        try:
            # Obtener las citas en orden descendente por fecha
            ordenCita = Cita.objects.order_by('-fecha_hora')
            serializer = CitaSerializer(ordenCita, many=True)

            data = ResponseData(
                Success=True,  # Indica que el proceso fue exitoso
                Status=status.HTTP_200_OK,  # Muestra el estado de la respuesta
                Message="Orden de las citas por fecha obtenido exitosamente",
                Record=serializer.data  # Datos actualizados a regresar al usuario
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except:
            data = ResponseData(
                Success=False,  # Indica que el proceso fue exitoso
                Status=status.HTTP_500_INTERNAL_SERVER_ERROR,  # Muestra el estado de la respuesta
                Message="Error al obtener el orden de las citas",
                Record=[]  # Datos actualizados a regresar al usuario
            )
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data.toResponse())

    @action(methods=['post'], detail=False)
    def AgendarCita(self, request, pk=None):
        try:
            paciente_id = request.data.get('paciente_id') or request.data.get('paciente')
            paciente = Paciente.objects.get(id=paciente_id)

            # Verifica si el usuario no es superusuario y no tiene permisos para agendar otra cita
            if not request.user.is_superuser:
                try:
                    paciente = Paciente.objects.get(id=paciente_id)
                    # Verifica si el paciente no pertenece al usuario autenticado
                    if paciente.usuario_id != request.user.id:
                        return Response({
                            "Success": False,
                            "Status": status.HTTP_403_FORBIDDEN,
                            "Message": "No tiene permiso para agendar una cita para otro paciente.",
                            "Record": []
                        }, status=status.HTTP_403_FORBIDDEN)
                except Paciente.DoesNotExist:
                    return Response({
                        "Success": False,
                        "Status": status.HTTP_404_NOT_FOUND,
                        "Message": "Paciente no encontrado.",
                        "Record": []
                    }, status=status.HTTP_404_NOT_FOUND)


            # Validación en el caso de que el paciente esté inactivo, es decir que fue anulado
            if not paciente.activo:
                data = ResponseData(
                    Success=False,  # Si el proceso no se ejecutó correctamente
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message="No se puede agendar una cita para un paciente que fue anulado",  # Mensaje para el usuario
                    Record=[]
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

                # Validación para doctor activo
            doctor_id = request.data.get('doctor')
            doctor = Doctor.objects.get(id=doctor_id)
            if not doctor.activo:
                    data = ResponseData(
                        Success=False,
                        Status=status.HTTP_400_BAD_REQUEST,
                        Message="El doctor está inactivo y no puede ser asignado para esta cita",
                        Record=[]
                    )
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())



            # Parsear fecha y hora de la solicitud
            fecha_hora = parser.parse(request.data.get('fecha_hora'))

            # Convertir tanto la fecha actual como la fecha_hora en "naive" (sin zona horaria)
            hora_actual = datetime.now()

            if fecha_hora.tzinfo is not None:
                fecha_hora = fecha_hora.replace(tzinfo=None)

            if hora_actual.tzinfo is not None:
                hora_actual = hora_actual.replace(tzinfo=None)

            # No se pueden agendar citas el mismo día
            if fecha_hora.date() == hora_actual.date():
                data = ResponseData(
                    Success=False,  # Si el proceso no se ejecutó correctamente
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message="No se permite agendar Citas para el mismo día",  # Mensaje para el usuario
                    Record=[]
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # Comprobar si la fecha_hora es al menos 30 minutos después de hora_actual
            if fecha_hora < hora_actual + timedelta(minutes=30):
                data = ResponseData(
                    Success=False,  # Si el proceso no se ejecutó correctamente
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message="No se puede agendar una Cita menos de 30 minutos antes del horario actual",#Mensaje para el usuario
                    Record=[]
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            hora_inicio_atencion = datetime.strptime("09:00", "%H:%M").time()
            hora_fin_atencion = datetime.strptime("17:00", "%H:%M").time()

            if fecha_hora.time() < hora_inicio_atencion or fecha_hora.time() > hora_fin_atencion:
                data = ResponseData(
                    Success=False,  # Si el proceso no se ejecutó correctamente
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message="El horario de la Cita debe estar dentro del horario de atención (9:00 am -5:00 pm)",
                    Record=[]
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            citas_del_dia = Cita.objects.filter(paciente=paciente, fecha_hora__date=fecha_hora.date())
            if citas_del_dia.exists():
                data = ResponseData(
                    Success=False,  # Si el proceso no se ejecutó correctamente
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message="El Paciente ya tiene una Cita agendada para ese día",
                    Record=[]
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # Verificación del doctor
            if Cita.objects.filter(fecha_hora=fecha_hora, doctor=request.data.get('doctor')).exists():
                doctores_ocupados = Cita.objects.filter(fecha_hora=fecha_hora).values_list('doctor', flat=True)
                doctor_original = Doctor.objects.get(id=request.data.get('doctor'))
                doctores_disponibles = Doctor.objects.exclude(id__in=doctores_ocupados).filter(
                    especialidad=doctor_original.especialidad)

                if doctores_disponibles.exists():
                    cita_data = request.data.copy()
                    cita_data['paciente'] = paciente_id
                    cita_data['fecha_hora'] = fecha_hora
                    cita_data['doctor'] = doctores_disponibles.first().id

                    # Validación de código único para la cita
                    if Cita.objects.filter(codigoCita=cita_data.get('codigoCita')).exists():
                        data = ResponseData(
                            Success=False,
                            Status=status.HTTP_400_BAD_REQUEST,
                            Message="El código de Cita ya existe",
                            Record=[]
                        )
                        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

                    serializer = CitaSerializer(data=cita_data)
                    if serializer.is_valid():
                        serializer.save()
                        data = ResponseData(
                            Success=True,  # Indica que el proceso fue exitoso
                            Status=status.HTTP_201_CREATED,  # Muestra el estado de la respuesta
                            Message="Cita agendada exitosamente con otro Doctor disponible",
                            Record=serializer.data  # Datos a regresar al usuario
                        )
                        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())
                    else:
                        data = ResponseData(
                            Success=False,  # Si el proceso no se ejecutó correctamente
                            Status=status.HTTP_400_BAD_REQUEST,
                            Message="Datos inválidos en la Cita", #Mensaje para el usuario
                            Record=[]
                        )
                        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

                else:
                    data = ResponseData(
                        Success=False,  # Si el proceso no se ejecutó correctamente
                        Status=status.HTTP_400_BAD_REQUEST,
                        Message="No hay doctores disponibles en la misma Especialidad en ese horario", #Mensaje para el usuario
                        Record=[]
                    )
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # Si el doctor está disponible, agenda la cita normalmente
            else:
                cita_data = request.data.copy()
                cita_data['paciente'] = paciente_id
                cita_data['fecha_hora'] = fecha_hora

                # Validación de código único para la cita
                if Cita.objects.filter(codigoCita=cita_data.get('codigoCita')).exists():
                    data = ResponseData(
                        Success=False,
                        Status=status.HTTP_409_CONFLICT,
                        Message="El código de Cita ya existe",
                        Record=[]
                    )
                    return Response(status=status.HTTP_409_CONFLICT, data=data.toResponse())

                serializer = CitaSerializer(data=cita_data)
                if serializer.is_valid():
                    serializer.save()
                    data = ResponseData(
                        Success=True,  # Indica que el proceso fue exitoso
                        Status=status.HTTP_201_CREATED,  # Muestra el estado de la respuesta
                        Message="Cita agendada exitosamente", #Mensaje para el usuario
                        Record=serializer.data  # Datos a regresar al usuario
                    )
                    return Response(status=status.HTTP_201_CREATED, data=data.toResponse())
                else:
                    data = ResponseData(
                        Success=False,  # Si el proceso no se ejecutó correctamente
                        Status=status.HTTP_400_BAD_REQUEST,
                        Message="Datos inválidos en la Cita", #Mensaje para el usuario
                        Record=[]
                    )
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        #except Paciente.DoesNotExist:
            #data = ResponseData(
              #  Success=False,  # Si el proceso no se ejecutó correctamente
              #  Status=status.HTTP_404_NOT_FOUND,
              #  Message="Paciente no encontrado",  # Mensaje para el usuario
               # Record=[]
            #)
           # return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

        except Doctor.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Doctor no encontrado", # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND,data=data.toResponse())

        except Recepcionista.DoesNotExist:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_404_NOT_FOUND,
                Message="Recepcionista no encontrado", # Mensaje para el usuario
                Record=[]
            )
            return Response(status=status.HTTP_404_NOT_FOUND,data=data.toResponse())

        except Exception as e:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                Message=f"Error inesperado al agendar la cita: {str(e)}",
                Record={}
            )
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data.toResponse())
