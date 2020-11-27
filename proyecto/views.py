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

@login_required
def home(request):
    return render(request, 'home.html')

from django.views.generic.list import ListView

class ver(ListView):
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

def crear_doctor(request):
    doctorForm = modelform_factory(models.Doctor, exclude=('funcionario_registrador','creacion'))
    if request.method == 'POST':
        doctor = doctorForm(request.POST)
        if doctor.is_valid():
            d = doctor.save(commit=False)
            d.funcionario_registrador = models.Funcionario.objects.get(usuario=request.user.id)
            d.save()
            messages.success(request, 'Doctor '+d.nombre+' añadido exitosamente.')
            return HttpResponseRedirect(reverse('ver', args=('doctores',)))
    else:
        doctor = doctorForm()

    return render(request, 'doctor/crear.html', {'form': doctor})

def crear_funcionario(request):
    funcionarioForm = modelform_factory(models.Funcionario, exclude=[])
    if request.method == 'POST':
        funcionario = funcionarioForm(request.POST)
        if funcionario.is_valid():
            f = funcionario.save()
            messages.success(request, 'Funcionario '+f.nombre+' añadido exitosamente.')
            return HttpResponseRedirect(reverse('ver', args=('funcionarios',)))
    else:
        funcionario = funcionarioForm()

    return render(request, 'funcionario/crear.html', {'form': funcionario})

from django.views.generic.detail import DetailView 

class perfil(DetailView): 
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['superpersonas'] = self.kwargs['superpersona']
        context['title_singular'] = self.kwargs['superpersona'][0:-1]
        context['title'] = self.kwargs['superpersona']
        return context

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

def borrar(request):
    raise Http404("TODO")