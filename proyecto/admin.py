from django.contrib import admin

# Register your models here.
from proyecto import models

admin.site.register(models.Paciente)
admin.site.register(models.Funcionario)
admin.site.register(models.Doctor)