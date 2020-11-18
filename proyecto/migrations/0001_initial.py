# Generated by Django 3.1.3 on 2020-11-18 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('universidad', models.CharField(max_length=100)),
                ('eps', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geolocalizacion', models.CharField(max_length=100)),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('ciudad_contagio', models.CharField(max_length=100)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('tipo_doc', models.CharField(choices=[('CC', 'Cédula de ciudadanía'), ('TI', 'Tarjeta de indentidad'), ('RC', 'Registro civil'), ('CE', 'Cédula de extranjería'), ('PA', 'Pasaporte')], max_length=22)),
                ('doc', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=255)),
                ('barrio', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('temperatura', models.DecimalField(decimal_places=2, max_digits=5)),
                ('peso', models.IntegerField()),
                ('presion_arterial', models.IntegerField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.doctor')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laboratorio', models.CharField(max_length=32)),
                ('cantidad', models.PositiveIntegerField()),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.medicamento')),
            ],
        ),
        migrations.AddField(
            model_name='paciente',
            name='parientes',
            field=models.ManyToManyField(related_name='pariente', to='proyecto.Persona'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.persona'),
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('clave', models.CharField(max_length=100)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.persona')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='funcionario_registrador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.funcionario'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.persona'),
        ),
    ]