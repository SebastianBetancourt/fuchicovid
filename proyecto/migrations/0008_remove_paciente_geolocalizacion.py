# Generated by Django 3.1.3 on 2020-11-30 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0007_paciente_geoubicacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='geolocalizacion',
        ),
    ]