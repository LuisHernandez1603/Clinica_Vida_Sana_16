from rest_framework.routers import DefaultRouter

from Apps.Movimientos.Doctor.API.DoctorAPI import DoctorViewSet

routerDoctor = DefaultRouter()

routerDoctor.register(prefix='Doctor', basename='Doctor', viewset=DoctorViewSet)
