from django.contrib import admin
from sigef.clientes.models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rfc', 'nombre', 'apellidos')
    search_fields = ['rfc', 'nombre', 'apellidos']

admin.site.register(Cliente)

