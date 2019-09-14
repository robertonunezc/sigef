from django.conf.urls import url
from sigef.egresos import views
app_name = 'egresos'
urlpatterns = [
     url(r'nuevo', views.nuevo_egreso, name='nuevo_egreso'),
     url(r'listado', views.listado_egresos, name='listado_egresos'),
     url(r'cargar-factura', views.cargar_factura, name='cargar_factura'),
     url(r'pago-factura', views.pago_factura, name='pago_factura'),
     url(r'actualizar-facturas', views.actualizar_facturas, name='actualizar_facturas'),
     url(r'proveedor-add', views.nuevo_proveedor, name='nuevo_proveedor'),
 ]