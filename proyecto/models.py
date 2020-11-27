from django.db import models
from django.contrib.auth.models import User

# Modelo de datos

class Persona(models.Model):
    CC = 'CC'
    TI = 'TI'
    RC = 'RC'
    CE = 'CE'
    PA = 'PA'
    TIPO_DOCUMENTO_CHOICES = [
        (CC, 'Cédula de ciudadanía'),
        (TI, 'Tarjeta de indentidad'),
        (RC, 'Registro civil'),
        (CE, 'Cédula de extranjería'),
        (PA, 'Pasaporte')
    ]
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    tipo_doc = models.CharField(max_length=22, choices=TIPO_DOCUMENTO_CHOICES)
    doc = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    barrio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=32)
    def __str__(self):
        return '{} {}'.format(self.apellido, self.nombre)


class Funcionario(Persona):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

class Doctor(Persona):
    funcionario_registrador = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    creacion = models.DateTimeField(auto_now_add=True)
    universidad = models.CharField(max_length=100)
    eps = models.CharField(max_length=100)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

class Paciente(Persona):
    geolocalizacion = models.CharField(max_length=100)
    doctor_encargado = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    creacion = models.DateTimeField(auto_now_add=True)
    ciudad_contagio = models.CharField(max_length=100)
    parientes = models.ManyToManyField(Persona, related_name='pariente')

class Visita(models.Model):
    fecha = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    peso = models.IntegerField()
    presion_arterial = models.IntegerField()

class Medicamento(models.Model):
    nombre = models.CharField(max_length=32)

class Reserva(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    laboratorio = models.CharField(max_length=32)
    cantidad = models.PositiveIntegerField()



# Trigger
from django.db import connection
print("models being executed")
connection.cursor().execute("""
CREATE OR REPLACE FUNCTION reabastecer_medicamento()
RETURNS trigger AS '
BEGIN
  IF NEW.cantidad = 0 THEN
    NEW.cantidad := 100;
  END IF;
  RETURN NEW;
END' LANGUAGE 'plpgsql'""")

connection.cursor().execute("DROP TRIGGER IF EXISTS medicamento_acabado ON proyecto_reserva")

connection.cursor().execute("""
CREATE TRIGGER medicamento_acabado 
BEFORE UPDATE ON proyecto_reserva 
FOR EACH ROW EXECUTE 
PROCEDURE reabastecer_medicamento();""")