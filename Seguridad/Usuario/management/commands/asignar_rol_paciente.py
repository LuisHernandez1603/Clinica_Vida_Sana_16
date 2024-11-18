from django.core.management.base import BaseCommand
from Seguridad.Usuario.models import Usuario  # Importa tu modelo desde 'usuario'

class Command(BaseCommand):
    help = 'Asigna el rol de paciente a un usuario'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        try:
            # Obtener el usuario por su nombre de usuario
            usuario = Usuario.objects.get(username=options['username'])
            # Asignar el rol de paciente
            usuario.role = 'paciente'
            usuario.save()
            self.stdout.write(self.style.SUCCESS(f'Rol de paciente asignado a {usuario.username}'))
        except Usuario.DoesNotExist:
            self.stdout.write(self.style.ERROR('Usuario no encontrado'))