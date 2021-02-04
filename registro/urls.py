from django.urls import include, path, re_path
from django.conf import settings
from registro import views

urlpatterns = [
	re_path('^reportes/$', views.reports),
	re_path('^censo/$', views.censo),
	re_path('^censo/ingreso/$', views.censo_ingreso),
	re_path('^censo/servicio/$', views.censo_servicio),
	re_path('^censo/paciente/detalle/$', views.censo_paciente_detalle),
	re_path('^censo/salida/$', views.censo_salida),
	re_path('^censo/paciente/buscar/$', views.censo_paciente_buscar),
]