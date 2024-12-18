# Generated by Django 4.2.16 on 2024-11-13 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Cita', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('diagnostico', models.TextField()),
                ('recomendaciones', models.TextField()),
                ('codigo_Consulta', models.CharField(max_length=5)),
                ('activo', models.BooleanField(default=True)),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Cita.cita')),
            ],
        ),
    ]
