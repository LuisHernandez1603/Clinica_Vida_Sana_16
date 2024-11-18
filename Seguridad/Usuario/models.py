from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Usuario(AbstractUser):
    ROLE_CHOICES = [
        ('paciente', 'Paciente'),
        # ('doctor', 'Doctor'),  # Puedes agregar otros roles si es necesario
        ('administrador', 'Administrador'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'Usuario'