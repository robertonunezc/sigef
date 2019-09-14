from datetime import datetime, date
from xml.dom import minidom

from decimal import Decimal

from django.forms import inlineformset_factory
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
from sigef import settings
from sigef.egresos.forms import FacturaForm, ProveedorForm, ConceptoForm
from sigef.main.models import Empresa
from sigef.egresos.models import *
from sigef.main.models import TipoProveedor
from sigef.egresos.serializers import ProveedorSerializer

@login_required
def listado_egresos(request):
    conceptos = Concepto.objects.all()
    context = {
        'conceptos': conceptos
    }
    return render(request, 'egresos/listado_egresos.html', context=context)


@login_required
def nuevo_egreso(request):
    form = FacturaForm()
    form_proveedor = ProveedorForm()
    msg = None
    tipo_proveedor = TipoProveedor.objects.all()
    if request.method == 'POST':
        form = FacturaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_factura = request.FILES.get('xml')
            form.save()
            json_data = parseXML(archivo_factura)
            print(json_data)

            context = {
                'form': form,
                'form_proveedor': form_proveedor,
                'tipo_proveedor': tipo_proveedor,
                'msg': "Factura guardada con éxito"
            }
            return render(request, 'egresos/nuevo_egreso.html', context=context)
    context = {
        'form': form,
        'form_proveedor': form_proveedor,
        'msg': msg,
        'tipo_proveedor': tipo_proveedor
    }
    return render(request, 'egresos/nuevo_egreso.html', context=context)


@login_required
def nuevo_proveedor(request):
    if request.method == 'POST':
        form_proveedor = ProveedorForm(request.POST)
        if form_proveedor.is_valid():
            nuevo_proveedor = form_proveedor.save()
            serializer = ProveedorSerializer([nuevo_proveedor], many=True)
            json_data = {
                'msg': 'OK',
                'rc': 0,
                'data': serializer.data
            }
            return HttpResponse(json.dumps(json_data), content_type='application/json')
    json_data = {
        'msg': 'Error intentando crear un proveedor',
        'rc': 0,
        'data': 'null'
    }
    return HttpResponse(json.dumps(json_data), content_type='application/json')


@login_required
def cargar_factura(request):
    archivo_factura = request.FILES.get('facturaFile')

    if not archivo_factura:
        json_data = {'rc': -1, 'msg': 'Debe cargar una factura'}
        return HttpResponse(json.dumps(json_data), content_type='application/json')

    json_data = parseXML(archivo_factura)
    print(json_data)
    return HttpResponse(json.dumps(json_data), content_type='application/json')


@login_required
def pago_factura(request):
    json_data = {'rc': -1, 'msg': "Intente de nuevo"}
    if request.method == 'POST':
        id_factura = request.POST['id_factura']
        monto = Decimal(request.POST['monto'])
        fecha = request.POST['fecha']
        fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        try:
            factura = Factura.objects.get(pk=id_factura)
            if monto > factura.monto_x_pagar():
                json_data = {'rc': -2, 'msg': 'El monto es mayor a la cantidad por pagar.'}
            else:
                pago = Pago()
                pago.factura = factura
                pago.monto = monto
                pago.fecha = fecha
                factura.monto_pagado = factura.monto_pagado + monto
                pago.save()
                factura.save()
                json_data = {'rc': 0, 'msg': 'El pago se ha registrado.'}
        except Factura.DoesNotExist:
            json_data = {'rc': -1, 'msg': 'La factura no existe.'}

    return HttpResponse(json.dumps(json_data), content_type='application/json')


def actualizar_facturas(request):
    facturas = Factura.objects.filter(estado__estado='ABIERTA')
    hoy = date.today()
    atrasada_estado = resolverEstado('ATRASADA')
    for factura in facturas:
        if factura.fecha_limite_pago < hoy:
            factura.estado = atrasada_estado
            factura.save()
    return HttpResponse(json.dumps({'rc': 0, 'msg': 'OK'}), content_type='application/json')


def validarRFC(rfc_receptor):
    empresa = Empresa.objects.first()
    return empresa and empresa.rfc == rfc_receptor


def datosValidos(datos_xml):
    receptor = datos_xml.getElementsByTagName('cfdi:Receptor')
    rfc_receptor = receptor[0].attributes['Rfc'].value
    return validarRFC(rfc_receptor)


def resolverEmisor(datos_emisor):
    rfc_emisor = datos_emisor.attributes['Rfc'].value
    try:
        proveedor = Proveedor.objects.get(rfc=rfc_emisor)
        return {'tiene': True,
                'id': proveedor.id,
                'rfc': proveedor.rfc,
                'razon_social': proveedor.razon_social,
                'telefono_contacto': proveedor.telefono_contacto,
                'email_contacto': proveedor.email_contacto}
    except Proveedor.DoesNotExist:
        razon_social = datos_emisor.attributes['Nombre'].value
        return {'tiene': False,
                'id': -1,
                'rfc': rfc_emisor,
                'razon_social': razon_social}


def resolverEstado(estado = 'ABIERTA'):
    try:
        estado_obj = EstadoFactura.objects.get(estado=estado)
    except EstadoFactura.DoesNotExist:
        estado_obj = EstadoFactura()
        estado_obj.estado = estado
        estado_obj.save()
    return estado_obj


def resolverMoneda(nomenclador_moneda):
    try:
        moneda = TipoMoneda.objects.get(nomenclatura=nomenclador_moneda)
    except TipoMoneda.DoesNotExist:
        moneda = TipoMoneda()
        moneda.moneda = nomenclador_moneda
        moneda.nomenclatura = nomenclador_moneda
        moneda.save()
    return moneda.to_json()


def resolverUnidad(clave_unidad):
    try:
        unidad = TipoUnidad.objects.get(clave=clave_unidad)
    except TipoUnidad.DoesNotExist:
        unidad = TipoUnidad()
        unidad.unidad = clave_unidad
        unidad.clave = clave_unidad
        unidad.save()
    return unidad


def resolverConceptos(datos_conceptos):
    conceptos = []
    for concepto in datos_conceptos:
        unidad = resolverUnidad(concepto.attributes['ClaveUnidad'].value)
        factura = Factura.objects.last()
        importe = float(concepto.attributes['Importe'].value)
        valor_unitario = float(concepto.attributes['ValorUnitario'].value)
        concepto_obj = Concepto()
        concepto_obj.clave_prod_serv = concepto.attributes['ClaveProdServ'].value
        concepto_obj.cantidad = concepto.attributes['Cantidad'].value
        concepto_obj.descripcion = concepto.attributes['Descripcion'].value
        concepto_obj.valor_unitario = valor_unitario
        concepto_obj.importe = importe
        concepto_obj.unidad = unidad
        concepto_obj.factura = factura
        concepto_obj.precio_venta_base = valor_unitario * 1.50
        concepto_obj.descuento_maximo = valor_unitario * 1.25
        concepto_obj.save()
    return conceptos


def getDatos(datos_xml):
    datos_factura = datos_xml.getElementsByTagName('cfdi:Comprobante')
    total = datos_factura[0].attributes['Total'].value
    total = Decimal(total)
    numero = datos_factura[0].attributes['Folio'].value
    fecha = datos_factura[0].attributes['Fecha'].value
    fecha = fecha.split('T', 1)[0]
    fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
    datos_emisor = datos_xml.getElementsByTagName('cfdi:Emisor')
    datos_proveedor = resolverEmisor(datos_emisor[0])
    estado = resolverEstado()
    nomenclador_moneda = datos_factura[0].attributes['Moneda'].value
    moneda = resolverMoneda(nomenclador_moneda)
    datos_conceptos = datos_xml.getElementsByTagName('cfdi:Concepto')
    conceptos = resolverConceptos(datos_conceptos)
    return {'msg': 'ok',
            'rc': 0,
            'data': {'numero': numero,
                     'monto': total.__str__(),
                     'fecha_emision': fecha.isoformat(),
                     'monto_pagado': 0,
                     'proveedor': datos_proveedor,
                     'estado': estado.id,
                     'moneda': moneda,
                     'conceptos': conceptos
                     }
            }


def parseXML(archivo_factura):
    base_dir = settings.MEDIA_ROOT
    datos_xml = minidom.parse('{}/facturas/{}'.format(base_dir,archivo_factura))
    return getDatos(datos_xml)
    # if datosValidos(datos_xml):
    #     return getDatos(datos_xml)
    # else:
    #     return {'rc': -1, 'msg': 'Receptor inválido, verifique la configuración.'}
