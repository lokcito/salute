from django.shortcuts import render
from registro.models import FileDataReport, \
	Servicio, Paciente, Censo
from pytz import timezone, UTC
from datetime import datetime, time, timedelta
from registro.utils import scrapfile,\
	 datetime_now, get_file_data, get_dict_from_data,\
	 get_services, get_valid_rows, \
	 paciente_get_or_create
from django.http import JsonResponse
from django.http import HttpResponseRedirect, \
	HttpResponse, QueryDict
from registro.forms import ServicioForm, \
	CensoIngresoForm

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

	_dni = request.POST.get("dni", "-")
	paciente = paciente_get_or_create(_dni)
	if paciente is None:
		return HttpResponseRedirect("/404/")

	return HttpResponseRedirect(
		"/integracion/censo/ingreso/"\
			"?dni=%s&fist_name=%s&last_name=%s" % (
			paciente.dni,
			paciente.nombre,
			paciente.apellido
		))

def censo(request):
	context = {
		'censos': Censo.objects.filter(tipo = 'IN')
	}

	return render(request, 'censo.html', context)

def censo_ingreso(request):
	if request.method == "POST":
		_POST = request.POST.copy()
		_POST['tipo'] = 'IN'
		_POST['alta'] = 0
		_POST['usuario'] = 'ss'
		form = CensoIngresoForm(_POST)
		if not form.is_valid():
			print("<>|", form.errors)
			return HttpResponseRedirect("/404/")

		form.save()
		return HttpResponseRedirect("/integracion/censo/")

	_dni = request.GET.get("dni", "-")
	if _dni == "-":
		return HttpResponseRedirect("/404/")

	paciente = Paciente.objects.filter(dni = _dni).first()

	if paciente is None:
		return HttpResponseRedirect("/404/")


	context = {
		'servicios': Servicio.objects.all().order_by('-fecha'),
		'paciente': paciente
	}

	return render(request, 'censo_ingreso.html', context)

def censo_servicio(request):
	if request.method == 'POST':
		form = ServicioForm(request.POST)
		if not form.is_valid():
			return HttpResponseRedirect("/integracion/censo/servicio/")

		form.save()

		return HttpResponseRedirect("/integracion/censo/servicio/?reload=%s" % (datetime.now()))

	context = {
		'services': ['xxx', 'yyyy'],
		'list': Servicio.objects.all().order_by('-fecha')
	}
	return render(request, 'censo_servicio.html', context)

def censo_paciente_detalle(request):
	context = {}
	return render(request, 'censo_paciente_detalle.html', context)

def censo_salida(request):
	context = {}
	return render(request, 'censo_salida.html', context)
