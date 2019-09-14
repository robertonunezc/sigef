from django.conf.urls import url
from sigef.main import views
app_name = 'main'
urlpatterns = [
     url(r'menu-principal', views.inicio, name='inicio'),
 ]