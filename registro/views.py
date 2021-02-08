from django.shortcuts import render
from registro.models import FileDataReport, \
	Servicio, Paciente, Censo
from pytz import timezone, UTC
from datetime import datetime, time, timedelta
from registro.utils import scrapfile,\
	 datetime_now, get_file_data, get_dict_from_data,\
	 get_services, get_valid_rows, \
	 paciente_get_or_create, auth_essalud, \
	 scrap_services
from django.http import JsonResponse
from django.http import HttpResponseRedirect, \
	HttpResponse, QueryDict
from registro.forms import ServicioForm, \
	CensoIngresoForm, CensoSalidaForm

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

	auth_essalud()

	return HttpResponseRedirect(
		"/integracion/censo/ingreso/"\
			"?took=true&dni=%s&fist_name=%s&last_name=%s" % (
			paciente.dni,
			paciente.nombre,
			paciente.apellido
		))

def censo(request):
	context = {
		'censos': Censo.objects.filter(gone = False, 
				servicio_id = request.GET.get('censo_id'))
	}

	return render(request, 'censo.html', context)

def censo_salidas(request):
	context = {
		'censos': Censo.objects.\
			filter(gone = True, 
				servicio_id = request.GET.get('censo_id'))
	}

	return render(request, 'censo.html', context)
	
def censo_ingreso(request):
	if request.method == "POST":
		_POST = request.POST.copy()
		_POST['gone'] = 0
		_POST['salida'] = '-'
		_POST['alta'] = 0
		_POST['usuario'] = 'ss'
		_POST['transferencia'] = _POST.get('transferencia', '-')
		if len(_POST['transferencia']) <= 0:
			_POST['transferencia'] = '-'
		form = CensoIngresoForm(_POST)
		if not form.is_valid():
			print("<>|", form.errors)
			return HttpResponseRedirect("/404/")

		form.save()
		return HttpResponseRedirect("/integracion/censo/?censo_id=" + _POST['servicio'])
	
	context = {
		'servicios': Servicio.objects.all().order_by('-fecha'),
	}
	
	_took = request.GET.get("took", "-")
	if _took == "-":
		return render(request, 'censo_ingreso.html', context)
	

	_dni = request.GET.get("dni", "-")
	if _dni == "-":
		return HttpResponseRedirect("/404/")

	paciente = Paciente.objects.filter(dni = _dni).first()

	context['paciente'] = paciente

	if paciente is None:
		return HttpResponseRedirect("/404/")

	return render(request, 'censo_ingreso.html', context)

def censo_servicio(request):
	if request.method == 'POST':
		form = ServicioForm(request.POST)
		if not form.is_valid():
			return HttpResponseRedirect("/integracion/censo/servicio/")

		form.save()

		return HttpResponseRedirect("/integracion/censo/servicio/?reload=%s" % (datetime.now()))

	context = {
		'services': scrap_services(),
		'list': Servicio.objects.all().order_by('-fecha')
	}
	return render(request, 'censo_servicio.html', context)

def censo_paciente_detalle(request):
	context = {}
	_id = request.GET.get('censo_id', '-')
	
	if _id == '-':
		return HttpResponseRedirect("/404/")
	
	context['censo'] = Censo.objects.get(id = _id)
	
	return render(request, 'censo_paciente_detalle.html', context)

def censo_salida(request):
	if request.method == "POST":
		censo = Censo.objects\
			.get(id = request.POST.get("censo_id"))
		
		if censo.gone:
			return HttpResponseRedirect(censo.get_link())
		
		POST = request.POST.copy()
		POST["gone"] = "1"
		
		POST['salida'] = POST.get('salida', '-')
		if len(POST['salida']) <= 0:
			POST['salida'] = '-'
			
		form = CensoSalidaForm(POST, instance = censo)
		if not form.is_valid():
			print(">", form.errors)
			return HttpResponseRedirect("/404/")
			
		form.save()
		return HttpResponseRedirect(censo.get_link())
			
	context = {}

	_id = request.GET.get('censo_id', '-')
	
	if _id == '-':
		return HttpResponseRedirect("/404/")
	
	context['censo'] = Censo.objects.get(id = _id)
	
	# context['outputs'] = context['censo'].get_outputs()
	if context['censo'].gone:
		return HttpResponseRedirect(context['censo'].get_link())
	# if context['outputs'].exists():
	# 	return HttpResponseRedirect(context['censo'].get_link())
	
	return render(request, 'censo_salida.html', context)
