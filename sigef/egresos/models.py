import datetime
from datetime import date
from django.core.validators import RegexValidator
from django.db import models
from sigef.main.models import TipoMoneda, TipoCredito, CategoriaTipoProveedor, EstadoFactura, TipoUnidad


# Create your models here.

# Tablas del negocio
class Proveedor(models.Model):
    rfc = models.CharField(max_length=13, unique=True, default='RFC', validators=[
        RegexValidator(
            regex='^.{12,13}$',
            message='El R.F.C. debe tener 12 o 13 caracteres.'
        )
    ])
    razon_social = models.CharField(max_length=250, unique=True)
    descripcion = models.CharField(max_length=250)
    telefono_contacto = models.CharField(max_length=15, null=True, blank=True)
    email_contacto = models.EmailField(unique=True, null=True, blank=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return "{}-{}".format(self.razon_social, self.rfc)

        # def cant_facturas(self):
        #     return self.facturas.count()


class Factura(models.Model):
    xml = models.FileField(upload_to='facturas/', null=True, blank=True)


class Concepto(models.Model):
    clave_prod_serv = models.CharField(max_length=250)
    cantidad = models.DecimalField(max_digits=14, decimal_places=2)
    descripcion = models.CharField(max_length=250)
    valor_unitario = models.DecimalField(max_digits=14, decimal_places=2)
    importe = models.DecimalField(max_digits=14, decimal_places=2)
    unidad = models.ForeignKey(TipoUnidad, on_delete=models.SET_NULL, null=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='conceptos')
    descuento_maximo = models.DecimalField(max_digits=8, decimal_places=2)
    precio_venta_base = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.descripcion


class Pago(models.Model):
    monto = models.DecimalField(max_digits=14, decimal_places=4)
    fecha = models.DateField()
    fecha_alta = models.DateTimeField(auto_now_add=True)
    factura = models.ForeignKey(Factura, on_delete=models.SET_NULL, null=True, related_name='pagos')

    def __str__(self):
        return "{}-{}".format(self.monto, self.factura)
