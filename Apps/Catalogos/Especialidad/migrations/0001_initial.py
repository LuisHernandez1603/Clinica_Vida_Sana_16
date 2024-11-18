# Generated by Django 4.2.16 on 2024-10-27 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('codigo_interno', models.CharField(max_length=5)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
    ]
