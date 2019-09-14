from django.contrib import admin
from sigef.egresos.models import Proveedor, Concepto


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('rfc', 'razon_social', 'descripcion', 'telefono_contacto', 'email_contacto', 'fecha_alta')
    search_fields = ['rfc', 'razon_social', 'descripcion', 'telefono_contacto', 'email_contacto']
    list_filter = ['fecha_alta']


admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Concepto)
