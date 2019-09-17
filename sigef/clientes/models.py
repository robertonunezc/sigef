
from django.db import models
# Create your models here.

# Tablas del negocio
class Cliente(models.Model):
    #comprobante = models.ForeignKey(Comprobante)
    rfc = models.CharField(max_length=23)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=60)