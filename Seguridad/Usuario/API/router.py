from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('logiToken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logiToken/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]