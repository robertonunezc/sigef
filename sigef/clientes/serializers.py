from rest_framework import serializers
from sigef.clientes.models import Cliente

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = ('rfc', 'nombre', 'apellidos')