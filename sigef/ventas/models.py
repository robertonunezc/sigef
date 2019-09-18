
from django.db import models
from sigef.clientes.models import Cliente
from sigef.egresos.models import Concepto
# Create your models here.

# Tablas del negocio
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING,)
    conceptos = models.ManyToManyField(Concepto)

