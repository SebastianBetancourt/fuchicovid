from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import proyecto.models as models

def index(request):
    template = loader.get_template('index.html')
    context = {'r' : 5}
    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.contrib.auth.decorators import login_required, permission_required

@login_required
def home(request):
    return render(request, 'home.html')

from django.views.generic.list import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin

class ver(PermissionRequiredMixin, ListView):
    template_name = 'persona/ver.html'
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        if kwargs['superpersona'] == 'pacientes':
            self.model = models.Paciente
        elif kwargs['superpersona'] == 'doctores':
            self.model = models.Doctor
        elif  kwargs['superpersona'] == 'funcionarios':
            self.model = models.Funcionario
        elif  kwargs['superpersona'] == 'parientes':
            self.model = models.Persona
        super().setup(request, *args, **kwargs)

    def get_queryset(self):
        medico = models.Doctor.objects.filter(usuario=self.request.user.id).first()
        if medico is not None:
            return models.Paciente.objects.filter(doctor_encargado_id=medico.id)
        return super().get_queryset()

    def get_permission_required(self):
        print(self.request.user.get_all_permissions())
        if self.kwargs['superpersona'] == 'pacientes':
            print('proyecto.view_paciente needed')
            return ['proyecto.view_paciente']
        elif self.kwargs['superpersona'] == 'doctores':
            return ['proyecto.view_doctor']
        elif self.kwargs['superpersona'] == 'funcionarios':
            return ['proyecto.view_funcionario']
        elif self.kwargs['superpersona'] == 'parientes':
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['superpersonas'] = self.kwargs['superpersona']
        context['title'] = self.kwargs['superpersona']
        context['crear'] = 'crear_'+self.kwargs['superpersona']
        return context

from django.forms import modelformset_factory, modelform_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

@permission_required('proyecto.add_paciente')
def crear_paciente(request):
    pacienteForm = modelform_factory(models.Paciente, exclude=('geolocalizacion','parientes'))
    parientesFormset = modelformset_factory(models.Persona, extra=3, max_num=100, fields=('nombre','apellido','email','tipo_doc','doc','direccion','barrio','telefono'))
    if request.method == 'POST':
        paciente = pacienteForm(request.POST)
        parientes = parientesFormset(request.POST)
        if paciente.is_valid() and parientes.is_valid():
            p = paciente.save()
            p.parientes.set(parientes.save())
            p.save()
            messages.success(request, 'Paciente '+p.nombre+' añadido exitosamente.')
            return HttpResponseRedirect(reverse('ver', args=('pacientes',)))
    else:
        paciente = pacienteForm()
        parientes = parientesFormset(queryset=models.Persona.objects.none())

    return render(request, 'paciente/crear.html', {'form': paciente, 'formParientes' : parientes})

from django.contrib.auth.models import Group

@permission_required('proyecto.add_doctor')
def crear_doctor(request):
    doctorForm = modelform_factory(models.Doctor, exclude=('funcionario_registrador','creacion'))
    if request.method == 'POST':
        doctor = doctorForm(request.POST)
        if doctor.is_valid():
            d = doctor.save(commit=False)
            d.funcionario_registrador = models.Funcionario.objects.get(usuario=request.user.id)
            Group.objects.get(name='doctores').user_set.add(d.usuario)
            d.save()
            messages.success(request, 'Doctor '+d.nombre+' añadido exitosamente.')
            return HttpResponseRedirect(reverse('ver', args=('doctores',)))
    else:
        doctor = doctorForm()

    return render(request, 'doctor/crear.html', {'form': doctor})

@permission_required('proyecto.add_funcionario')
def crear_funcionario(request):
    funcionarioForm = modelform_factory(models.Funcionario, exclude=[])
    if request.method == 'POST':
        funcionario = funcionarioForm(request.POST)
        if funcionario.is_valid():
            f = funcionario.save()
            Group.objects.get(name='funcionarios').user_set.add(f.usuario)
            messages.success(request, 'Funcionario '+f.nombre+' añadido exitosamente.')
            return HttpResponseRedirect(reverse('ver', args=('funcionarios',)))
    else:
        funcionario = funcionarioForm()

    return render(request, 'funcionario/crear.html', {'form': funcionario})

from django.views.generic.detail import DetailView 

class perfil(PermissionRequiredMixin, DetailView): 
    def setup(self, request, *args, **kwargs):
        if kwargs['superpersona'] == 'pacientes':
            self.model = models.Paciente
        elif kwargs['superpersona'] == 'doctores':
            self.model = models.Doctor
        elif  kwargs['superpersona'] == 'funcionarios':
            self.model = models.Funcionario
        elif  kwargs['superpersona'] == 'parientes':
            self.model = models.Persona
        super().setup(request, *args, **kwargs)

    def get_template_names(self):
        if self.kwargs['superpersona'] == 'pacientes':
            return ['paciente/perfil.html']
        elif self.kwargs['superpersona'] == 'doctores':
            return [ 'doctor/perfil.html']
        elif  self.kwargs['superpersona'] == 'funcionarios':
            return ['funcionario/perfil.html']
        elif  self.kwargs['superpersona'] == 'parientes':
            return ['persona/perfil.html']
        return super().get_template_names()

    def get_permission_required(self):
        if self.kwargs['superpersona'] == 'pacientes':
            return ['proyecto.view_paciente']
        elif self.kwargs['superpersona'] == 'doctores':
            return ['proyecto.view_doctor']
        elif self.kwargs['superpersona'] == 'funcionarios':
            return ['proyecto.view_funcionario']
        elif self.kwargs['superpersona'] == 'parientes':
            return []
        return super().get_permission_required()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['superpersonas'] = self.kwargs['superpersona']
        context['title_singular'] = self.kwargs['superpersona'][0:-1]
        context['title'] = self.kwargs['superpersona']
        if self.kwargs['superpersona'] == 'pacientes':
            context['visitas'] = models.Visita.objects.filter(paciente=self.kwargs['pk'])
        return context

@login_required
def editar(request, superpersona, pk):
    is_paciente = False
    parientes = []
    if superpersona == 'pacientes':
            is_paciente = True
            model = models.Paciente
            excluir = ['geolocalizacion','parientes']
    elif superpersona == 'doctores':
            model = models.Doctor
            excluir = ['funcionario_registrador','creacion']
    elif  superpersona == 'funcionarios':
            model = models.Funcionario
            excluir=[]
    elif  superpersona == 'parientes':
            model = models.Persona
            excluir=[]
    instance = model.objects.get(id=pk)
    form = modelform_factory(model, exclude=excluir)
    if is_paciente:
        parientesFormset = modelformset_factory(models.Persona, extra=3, max_num=3, fields=('nombre','apellido','email','tipo_doc','doc','direccion','barrio','telefono'))
    if request.method == 'POST':
        superpersonaForm = form(request.POST, instance=instance)
        if is_paciente:
            parientes = parientesFormset(request.POST)
        if superpersonaForm.is_valid() and ((not is_paciente) or parientes.is_valid()):
            superpersonaForm.save()
            if is_paciente:
                instance.parientes.add(*parientes.save())
                instance.save()
            messages.success(request, 'Perfil de '+instance.nombre+' editado exitosamente.')
            if superpersona == 'parientes':
                return HttpResponseRedirect(reverse('perfil', args=(superpersona, pk)))
            return HttpResponseRedirect(reverse('ver', args=(superpersona,)))
    else:
        superpersonaForm = form(instance=instance)
        if is_paciente:
            parientes = parientesFormset(queryset=instance.parientes.all())

    return render(request, 'persona/editar.html', {'form': superpersonaForm, 'formParientes' : parientes, 'superpersona': superpersona, 'pk' : pk, 'nombre' : instance.apellido+' '+instance.nombre})
    
from django.http import Http404

@login_required
def borrar(request, superpersona, pk):
    if superpersona == 'pacientes':
            model = models.Paciente
    elif superpersona == 'doctores':
            model = models.Doctor
    elif  superpersona == 'funcionarios':
            model = models.Funcionario
    elif  superpersona == 'parientes':
            model = models.Persona
    instancia = model.objects.get(id=pk)
    if superpersona == 'doctores' or superpersona == 'funcionarios':
             Group.objects.get(name=superpersona).user_set.remove(instancia.usuario)
    nombre = instancia.nombre
    deleted = instancia.delete()
    if deleted[0] > 0:
        
        messages.success(request, superpersona[:-1]+" "+nombre+" eliminado (también se borraron "+str(deleted[0]-1)+" registros relacionados).")
        return HttpResponseRedirect(reverse('ver', args=(superpersona,)))
    
@permission_required('proyecto.add_visita')
def crear_visita(request, pk):
    visitaForm = modelform_factory(models.Visita, exclude=('doctor','paciente','fecha'))
    if request.method == 'POST':
        visita = visitaForm(request.POST)
        if visita.is_valid():
            v = visita.save(commit=False)
            v.doctor = models.Doctor.objects.get(usuario=request.user.id)
            v.paciente =  models.Paciente.objects.get(id=pk)
            v.save()
            messages.success(request, 'Visita registrada exitosamente.')
            return HttpResponseRedirect(reverse('perfil', args=('pacientes',v.paciente.id)))
    else:
        visita = visitaForm()

    return render(request, 'visita/crear.html', {'form': visita, 'paciente' : models.Paciente.objects.get(id=pk)})

@permission_required('proyecto.view_reserva')
def medicamentos(request):
    reservas = models.Reserva.objects.all()
    medicamentos =  models.Medicamento.objects.all()
    tabla = []
    laboratorios = []
    for r in reservas:
        try:
            filaLaboratorio = laboratorios.index(r.laboratorio)
        except ValueError:
            laboratorios.append(r.laboratorio)
            tabla.append([r.laboratorio]+[0 for _ in medicamentos])
            filaLaboratorio = len(tabla) - 1
        try:
            colMedicamento = ([m.nombre for m in medicamentos].index(r.medicamento.nombre))+1
        except ValueError:
            medicamentos.append(r.medicamento.nombre)
            filaLaboratorio = len(medicamentos)
        tabla[filaLaboratorio][colMedicamento] = r.cantidad
    return render(request, 'medicamentos.html', {'reservas_objs': list(reservas.values()), 'tabla' : tabla, 'medicamentos' : medicamentos, 'laboratorios' : laboratorios })

@permission_required('proyecto.change_reserva')
def ordenar_medicamentos(request):
    if request.method == 'POST':
        r = request.POST
        reserva = models.Reserva.objects.get(laboratorio = r.get('laboratorio'), medicamento = models.Medicamento.objects.get(id=r.get('medicamento')))
        cantidad_solicitada = int(r.get('cantidad'))
        if reserva.cantidad < cantidad_solicitada:
            messages.error(request, 'La cantidad solicitada es mayor a la disponible en existencias')
        else:
            reserva.cantidad = reserva.cantidad - cantidad_solicitada
            reserva.save()
            messages.success(request,"Se ordenaron {} unds. de {} del laboratorio {} exitosamente.".format(cantidad_solicitada, reserva.medicamento.nombre, reserva.laboratorio))
        return HttpResponseRedirect(reverse('medicamentos'))

from django.db.models import Avg, Count
import json

@permission_required('proyecto.view_paciente')
def informe(request):
    if request.method == 'POST':
        r = request.POST
        total_visitas_rango = models.Visita.objects.filter(fecha__gte=r.get('desde'), fecha__lte=r.get('hasta')).count()
        return HttpResponse(json.dumps({'total': total_visitas_rango}), content_type="application/json")
    pacientes_barrio =  models.Paciente.objects.values("barrio").annotate(pacientes=Count("id"))
    edad_pacientes = models.Paciente.objects.all().values('edad').annotate(pacientes=Count("id"))
    estadisticas = {'total_pacientes': models.Paciente.objects.all().count(), 
                    'total_doctores': models.Doctor.objects.all().count(), 
                    'total_funcinarios': models.Funcionario.objects.all().count(), 
                    'promedio_por_barrio': models.Paciente.objects.values("barrio").annotate(pacientes=Count("id")).aggregate(Avg('pacientes')).get('pacientes__avg'),
                    'promedio_edad':  models.Paciente.objects.aggregate(Avg('edad')).get('edad__avg'),
                    'pacientes_barrio' :  {'pacientes' : [p.get('pacientes') for p in pacientes_barrio],'barrios' : [p.get('barrio') for p in pacientes_barrio]},
                    'edad_pacientes' : {'pacientes' : [e.get('pacientes') for e in edad_pacientes], 'edad' : [e.get('edad') for e in edad_pacientes]}
                    }
    return render(request, 'informe.html', estadisticas)
