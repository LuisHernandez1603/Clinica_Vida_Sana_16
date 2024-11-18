from rest_framework.routers import DefaultRouter
from Apps.Movimientos.Cita.API.CitaAPI import CitaViewSet

routerCita = DefaultRouter()

routerCita.register(prefix='Cita', basename='Cita', viewset=CitaViewSet)