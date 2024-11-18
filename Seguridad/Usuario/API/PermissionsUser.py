from rest_framework.permissions import BasePermission
from Apps.Catalogos.Paciente.models import Paciente

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



class IsPacienteOrSuperuser(BasePermission):
    """
    Permite el acceso solo al paciente dueño del registro o al superusuario.
    """
    def has_permission(self, request, view):
        # Permite acceso si el usuario es superusuario
        if request.user.is_superuser:
            return True

        # Obtiene el ID del paciente desde los datos de la solicitud
        paciente_id = request.data.get('paciente')
        if not paciente_id:
            return False

        # Verifica si el paciente está asociado al usuario autenticado
        try:
            paciente = Paciente.objects.get(id=paciente_id, usuario_id=request.user.id)
            return paciente.usuario_id == request.user.id
        except Paciente.DoesNotExist:
            return False

class IsPacienteOrSuperuserVerDatosDoctor(BasePermission):
    """
    Permiso para que solo los pacientes y superusuarios puedan acceder.
    """
    def has_permission(self, request, view):
        # Verificar si el usuario es un paciente o superusuario
        return request.user.is_authenticated and (request.user.is_superuser or hasattr(request.user, 'paciente'))

#class IsSuperuser(BasePermission):
        #def has_permission(self, request, view):
            # Permitir solo a los superusuarios
          #  return request.user.is_superuser

#from rest_framework.permissions import BasePermission

#class IsOwnPatient(BasePermission):

 #   """
  #  Permiso personalizado para permitir que un paciente vea y edite solo su propio registro.
   # """

    #def has_object_permission(self, request, view, obj):
     #       # Si el usuario está autenticado y es el paciente correspondiente
      #  return obj.usuario == request.user