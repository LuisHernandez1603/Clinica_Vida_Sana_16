from rest_framework.routers import DefaultRouter
from Apps.Catalogos.Paciente.API.PacienteAPI import PacienteViewSet

routerPaciente = DefaultRouter()

routerPaciente.register(prefix='Paciente', basename='Paciente', viewset=PacienteViewSet)
