from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


# Create your models here.


class Usuario(AbstractUser):
    objects = UserManager()
    telefono = models.IntegerField(blank=True, null=True)


# Tablas de control
class Empresa(models.Model):
    nombre = models.CharField(max_length=250)
    razon_social = models.CharField(max_length=250, unique=True)
    rfc = models.CharField(max_length=13, unique=True, default='RFC', validators=[
        RegexValidator(
            regex='^.{12,13}$',
            message='El R.F.C. debe tener 12 o 13 caracteres.'
        )
    ])

    class Meta:
        verbose_name_plural = "Empresa"

    def __str__(self):
        return self.nombre


class TipoProveedor(models.Model):
    tipo = models.CharField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = "Tipo proveedores"

    def __str__(self):
        return self.tipo

    def cant_categorias(self):
        return self.categorias.count()


class CategoriaTipoProveedor(models.Model):
    categoria = models.CharField(max_length=250, unique=True)
    tipo = models.ForeignKey(TipoProveedor,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name="categorias",
                             related_query_name="categoria")

    class Meta:
        verbose_name_plural = "Categorias tipo proveedor"

    def __str__(self):
        return self.categoria


class TipoCredito(models.Model):
    plazo = models.IntegerField(validators=[
        MinValueValidator(7, "El plazo debe ser mayor a 7 días."),
        MaxValueValidator(30, "El plazo máximo es de 30 días.")
    ], unique=True)

    def __str__(self):
        return self.plazo.__str__()


class EstadoFactura(models.Model):
    estado = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.estado


class TipoMoneda(models.Model):
    moneda = models.CharField(max_length=250, unique=True)
    nomenclatura = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.moneda

    def to_json(self):
        return {'id': self.id, 'moneda': self.moneda,
                'nomenclatura': self.nomenclatura}


class TipoCambioMoneda(models.Model):
    fecha = models.DateField()
    monto_mxn = models.DecimalField(max_digits=10,
                                    decimal_places=2)
    moneda = models.ForeignKey(TipoMoneda,
                               on_delete=models.SET_NULL,
                               null=True)

    def __str__(self):
        return self.moneda


class TipoUnidad(models.Model):
    unidad = models.CharField(
        max_length=250)
    clave = models.CharField(max_length=5,
                             unique=True)

    def __str__(self):
        return "{}-{}".format(self.unidad,
                              self.clave)

    def to_json(self):
        return {'id': self.id,
                'unidad': self.unidad,
                'clave': self.clave}
