"""
URL configuration for Config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Apps.Movimientos.Consulta.API.Urls import routerConsulta
from Seguridad.Usuario.API.UsuarioAPI import UserCreateView
from Apps.Catalogos.Especialidad.API.Urls import routerEspecialidad
from Apps.Catalogos.Paciente.API.Urls import routerPaciente
from Apps.Catalogos.Recepcionista.API.Urls import routerRecepcionista
from Apps.Movimientos.Cita.API.Urls import routerCita
from Apps.Movimientos.Doctor.API.Urls import routerDoctor
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(routerPaciente.urls)),
    path('api/', include(routerRecepcionista.urls)),
    path('api/', include(routerDoctor.urls)),
    path('api/', include(routerEspecialidad.urls)),
    path('api/', include(routerCita.urls)),
    path('api/', include(routerConsulta.urls)),
    path('api/', include('Seguridad.Usuario.API.router')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/register/', UserCreateView.as_view(), name='register-user')
]
