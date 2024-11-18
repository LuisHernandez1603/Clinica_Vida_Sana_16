from rest_framework.routers import DefaultRouter

from Apps.Catalogos.Recepcionista.API.RecepcionistaAPI import RecepcionistaViewSet

routerRecepcionista = DefaultRouter()

routerRecepcionista.register(prefix='Recepcionista', basename='Recepcionista', viewset=RecepcionistaViewSet)
