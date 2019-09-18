from django.contrib import admin
from sigef.clientes.models import Cliente
from sigef.egresos.models import Concepto
from sigef.ventas.models import Venta

class VentaAdmin(admin.ModelAdmin):
    list_display = (Cliente.rfc, Cliente.nombre, Cliente.apellidos, Concepto.descripcion)#, Concepto.cantidad)
    search_fields = [Cliente.rfc, Cliente.nombre, Cliente.apellidos, Concepto.descripcion]#, Concepto.cantidad]

admin.site.register(Venta)

