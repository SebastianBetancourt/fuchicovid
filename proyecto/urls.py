from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('ver/<superpersona>/', views.ver.as_view(), name='ver'),
    path('crear/paciente/', views.crear_paciente, name='crear_pacientes'),
    path('crear/doctor/', views.crear_doctor, name='crear_doctores'),
    path('crear/funcionario/', views.crear_funcionario, name='crear_funcionarios'),
    path('perfil/<superpersona>/<pk>', views.perfil.as_view(), name='perfil'),
    path('editar/<superpersona>/<pk>', views.editar, name='editar'),
    path('borrar/<superpersona>/<pk>', views.borrar, name='borrar'),
    path('registrar_visita/<pk>', views.crear_visita, name='crear_visita'),
    path('medicamentos/', views.medicamentos, name='medicamentos'),
    path('ordenar_medicamentos/', views.ordenar_medicamentos, name='ordenar_medicamentos'),
]