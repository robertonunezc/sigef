from django.conf.urls import url
from sigef.clientes import views
app_name = 'clientes'
urlpatterns = [
     url(r'nuevo', views.nuevo_cliente, name='nuevo_cliente'),
     url(r'listado', views.listado_clientes, name='listado_clientes'),

 ]