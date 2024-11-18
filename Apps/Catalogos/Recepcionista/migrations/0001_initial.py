# Generated by Django 4.2.16 on 2024-10-27 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recepcionista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=8)),
                ('correo_electronico', models.CharField(max_length=100, null=True)),
                ('fecha_ingreso', models.DateTimeField()),
                ('codigoRecepcionista', models.CharField(max_length=5)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
    ]