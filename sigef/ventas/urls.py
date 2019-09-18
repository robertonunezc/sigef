from django.conf.urls import url
from sigef.ventas import views
app_name = 'ventas'
urlpatterns = [
     url(r'nueva', views.nueva_venta, name='nueva_venta'),
     url(r'listado', views.listado_ventas, name='listado_ventas'),

 ]