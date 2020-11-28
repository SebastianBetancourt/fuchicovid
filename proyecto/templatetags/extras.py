from django import template

register = template.Library()

@register.filter(name='is_funcionario')
def is_funcionario(user):
    return user.groups.filter(name='funcionarios').exists()

@register.filter(name='is_doctor')
def is_doctor(user):
    return user.groups.filter(name='doctores').exists()