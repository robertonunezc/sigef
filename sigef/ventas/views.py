from datetime import datetime, date
from xml.dom import minidom

from decimal import Decimal

from django.forms import inlineformset_factory
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
from sigef.ventas.forms import VentasForm
from sigef.ventas.models import *
from sigef.ventas.serializers import VentasSerializer

@login_required
def listado_ventas(request):
    ventas = Venta.objects.all()
    context = {
        'ventas': ventas
    }
    return render(request, 'ventas/listado_ventas.html', context=context)


@login_required
def nueva_venta(request):
    form = VentasForm()
    msg = None
    if request.method == 'POST':
        form = VentasForm(request.POST)
        if form.is_valid():
            nueva_venta = form.save()
            serializer = VentasSerializer([nueva_venta], many=True)
            context = {
                'form': form,
                 'msg': "Venta guardada con éxito"
            }
            return render(request, 'ventas/nueva_venta.html', context=context)
    context = {
        'form': form,
        'msg': msg,
    }
    return render(request, 'ventas/nueva_venta.html', context=context)
