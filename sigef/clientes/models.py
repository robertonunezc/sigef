
from django.db import models

# Create your models here.

# Tablas del negocio
class Cliente(models.Model):
    rfc = models.CharField(max_length=23)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre + " " + self.apellidos + " (" + self.rfc + ")"