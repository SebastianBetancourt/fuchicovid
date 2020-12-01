from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from proyecto import models

# admin.site.register(models.Paciente)
admin.site.register(models.Funcionario)
admin.site.register(models.Doctor)

@admin.register(models.Paciente)
class PacienteAdmin(OSMGeoAdmin):
    default_lon = -8520000
    default_lat = 384000
    default_zoom = 8