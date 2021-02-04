from django.shortcuts import render
from registro.models import FileDataReport
from pytz import timezone, UTC
from datetime import datetime, time, timedelta
from registro.utils import scrapfile,\
	 datetime_now, get_file_data, get_dict_from_data,\
	 get_services, get_valid_rows
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
# Create your views here.
def reports(request):
	context = {}
	_force = request.GET.get('force', '-') == 'true'
	record_report  = get_file_data(force =_force )
	if record_report is None:
		return HttpResponseRedirect("/404/")
	context['record'] = record_report
	context['alldata'] = get_valid_rows(record_report.filename);
	context['services'] = get_services(record_report.filename)
	context['filtered'] = get_dict_from_data(record_report.filename)
	if _force:
		return HttpResponseRedirect("/integracion/reportes/")
	return render(request, 'report.html', context)

def censo_paciente_buscar(request):
	if request.method != 'POST':
		return HttpResponseRedirect("/404/")

	return HttpResponseRedirect(
		"/integracion/censo/ingreso/"\
			"?dni=%s&fist_name=%s&last_name=%s" % (
			'46004343',
			'ray',
			'rojas'
		))

def censo(request):
	context = {}

	return render(request, 'censo.html', context)

def censo_ingreso(request):
	context = {}
	return render(request, 'censo_ingreso.html', context)

def censo_servicio(request):
	context = {}
	return render(request, 'censo_servicio.html', context)

def censo_paciente_detalle(request):
	context = {}
	return render(request, 'censo_paciente_detalle.html', context)

def censo_salida(request):
	context = {}
	return render(request, 'censo_salida.html', context)
