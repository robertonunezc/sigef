from rest_framework import serializers
from sigef.egresos.models import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = ('id', 'rfc', 'razon_social','descripcion', 'telefono_contacto', 'email_contacto',
                  'fecha_alta')