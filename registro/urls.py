from django.urls import include, path, re_path
from django.conf import settings
from registro import views

urlpatterns = [
	re_path('^reportes/$', views.reports),

	re_path('^reportes/programacion$', views.reports_programacion),
	re_path('^censo/$', views.censo),
	re_path('^censo/ingreso/$', views.censo_ingreso),
	re_path('^censo/delete/$', views.censo_delete),
	re_path('^censo/servicio/$', views.censo_servicio),
	re_path('^censo/servicio/synced$', views.censo_servicio_synced),
	re_path('^censo/output/synced$', views.censo_output_synced),
	re_path('^censo/input/synced$', views.censo_input_synced),
	re_path('^censo/paciente/detalle/$', views.censo_paciente_detalle),
	re_path('^censo/salida/$', views.censo_salida),
	re_path('^censo/salidas/$', views.censo_salidas),
	re_path('^censo/paciente/buscar/$', views.censo_paciente_buscar),
]