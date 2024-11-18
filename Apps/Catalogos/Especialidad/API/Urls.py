from rest_framework.routers import DefaultRouter

from Apps.Catalogos.Especialidad.API.EspecialidadAPI import EspecialidadViewSet

routerEspecialidad = DefaultRouter()

routerEspecialidad.register(prefix='Especialidad', basename='Especialidad', viewset=EspecialidadViewSet)