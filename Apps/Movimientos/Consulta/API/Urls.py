from rest_framework.routers import DefaultRouter

from Apps.Movimientos.Consulta.API.ConsultaAPI import ConsultaViewSet

routerConsulta = DefaultRouter()
routerConsulta.register(prefix='Consulta', basename='Consulta', viewset=ConsultaViewSet)