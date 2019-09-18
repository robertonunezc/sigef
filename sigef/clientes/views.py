
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from sigef.clientes.forms import ClienteForm
from sigef.clientes.models import *
from sigef.clientes.serializers import ClienteSerializer

@login_required
def listado_clientes(request):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes
    }
    return render(request, 'clientes/listado_clientes.html', context=context)


@login_required
def nuevo_cliente(request):
    form = ClienteForm()
    msg = None
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nuevo_cliente = form.save()
            serializer = ClienteSerializer([nuevo_cliente], many=True)
            context = {
                'form': form,
                 'msg': "Cliente guardad con éxito"
            }
            return render(request, 'clientes/nuevo_cliente.html', context=context)
    context = {
        'form': form,
        'msg': msg,
    }
    return render(request, 'clientes/nuevo_cliente.html', context=context)
