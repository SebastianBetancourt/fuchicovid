from django.db import models

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

class Funcionario(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)

class Doctor(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    funcionario_registrador = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    creacion = models.DateTimeField(auto_now_add=True)
    universidad = models.CharField(max_length=100)
    eps = models.CharField(max_length=100)

class Paciente(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    geolocalizacion = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
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
