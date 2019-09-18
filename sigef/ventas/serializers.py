from rest_framework import serializers
from sigef.ventas.models import Venta
from sigef.clientes.models import Cliente
from sigef.egresos.models import Concepto

class VentasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venta
        fields = (Cliente.rfc, Cliente.nombre, Cliente.apellidos, Concepto.descripcion)#, Concepto.cantidad)