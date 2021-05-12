from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# Custom Decorator
def gerente_required(function):
    def _function(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        if not request.user.groups.filter(name='Gerente').exists():
            messages.info(request, 'No tiene los permisos para ingresar a esta sección')
            return HttpResponseRedirect(reverse_lazy('inicio'))
        return function(request, *args, **kwargs)
    return _function