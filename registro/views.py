from django.shortcuts import render
from django.contrib import messages

from registro.models import FileDataReport, \
	Servicio, Paciente, Censo
from pytz import timezone, UTC
from datetime import datetime, time, timedelta
from registro.utils import scrapfile,\
	 datetime_now, get_file_data, get_dict_from_data,\
	 get_services_from_file, get_valid_rows, \
	 paciente_get_or_create, auth_essalud, \
	 scrap_services, scrap_programacion
from django.http import JsonResponse
from django.http import HttpResponseRedirect, \
	HttpResponse, QueryDict
from registro.forms import ServicioForm, \
	CensoIngresoForm, CensoSalidaForm

def reports_programacion(request):
	context = {}
	data = scrap_programacion()
	
	context['data'] = data

	return render(request, 'reports_programacion.html', context)
# Create your views here.
def search_paciente_en_cesos(request):
	_dni = request.GET("dni", "-")
	if _dni == "-":
		return HttpResponseRedirect("/404/")
	o = Censo.objects.filter(paciente__dni = _dni)
	return render(request, 'censo_salidas.html', context)
	
def reports(request):
	context = {}
	_force = request.GET.get('force', '-') == 'true'
	record_report  = get_file_data(force =_force )
	if record_report is None:
		return HttpResponseRedirect("/404/")

	context['record'] = record_report
	context['alldata'] = get_valid_rows(record_report.filename);
	context['services'] = get_services_from_file(record_report.filename)
	context['filtered'] = get_dict_from_data(record_report.filename)
	if _force:
		return HttpResponseRedirect("/integracion/reportes/")
	return render(request, 'report.html', context)

def censo_paciente_buscar(request):
	if request.method != 'POST':
		return HttpResponseRedirect("/404/")

	servicio_id = request.POST.get("servicio_id")
	_dni = request.POST.get("dni", "-")
	paciente = paciente_get_or_create(_dni)
	if paciente is None:
		messages.info(request, "El DNI ingresado no es valido.")
		return HttpResponseRedirect("/integracion/censo/ingreso/")

	return HttpResponseRedirect(
		"/integracion/censo/ingreso/"\
			"?took=true&dni=%s&fist_name=%s&last_name=%s&servicio_id=%s" % (
			paciente.dni,
			paciente.nombre,
			paciente.apellido,
			servicio_id
		))

def censo(request):
	servicio_id = request.GET.get('servicio_id', '-')
	if servicio_id == '-':
		context = {
			'censos': Censo.objects.filter(salida_tipo = '---')
		}
	else:
		context = {
			'censos': Censo.objects.filter(salida_tipo = '---', 
					servicio_id = servicio_id),
			'servicio': Servicio.objects.get(id = servicio_id)
		}

	return render(request, 'censo.html', context)


def censo_by_paciente(request):

	dni = request.GET.get('dni', '-')
	if dni == '-':
		context = {
			'censos': Censo.objects.filter().\
				exclude(salida_tipo = '---')

		}
	else:
		context = {
			'censos': Censo.objects.\
				filter(servicio_id = request.GET.get('servicio_id')).\
				exclude(salida_tipo = '---'),
			'servicio': Servicio.objects.get(id = servicio_id)

		}


	return render(request, 'censo_salidas.html', context)

def censo_salidas(request):

	servicio_id = request.GET.get('servicio_id', '-')
	if servicio_id == '-':
		context = {
			'censos': Censo.objects.filter().\
				exclude(salida_tipo = '---')

		}
	else:
		context = {
			'censos': Censo.objects.\
				filter(servicio_id = request.GET.get('servicio_id')).\
				exclude(salida_tipo = '---'),
			'servicio': Servicio.objects.get(id = servicio_id)

		}


	return render(request, 'censo_salidas.html', context)
	
def censo_ingreso(request):
	if request.method == "POST":
		_POST = request.POST.copy()
		_POST['salida_tipo'] = '---'
		_POST['salida'] = '-'
		_POST['salida_servicio'] = 0
		_POST['usuario'] = 'ss'
		_POST['transferencia'] = _POST.get('transferencia', '-')
		if len(_POST['transferencia']) <= 0:
			_POST['transferencia'] = '-'
		form = CensoIngresoForm(_POST)
		if not form.is_valid():
			messages.info(request, form.errors)
			return HttpResponseRedirect("/integracion/censo/ingreso/")

		form.save()
		return HttpResponseRedirect("/integracion/censo/?servicio_id=" + _POST['servicio'])
	
	servicio_id = request.GET.get("servicio_id", "-")
	if servicio_id == "-":
		return HttpResponseRedirect("/404/")

	context = {
		'servicios': Servicio.objects.filter(id = servicio_id).order_by('-fecha'),
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
		_now = datetime_now()
		
		

		o = Servicio.objects.filter(fecha__year = _now.strftime('%Y'), 
			fecha__month = _now.strftime('%m'),
			fecha__day = _now.strftime('%d'), 
			nombre = request.POST.get("nombre"),
			estacion = request.POST.get("estacion"),
			habitacion = request.POST.get("habitacion"))

		if o.exists():
			messages.info(request, 
				"El servicio ya ha sido creado en la fecha: %s" % (_now.strftime('%Y-%m-%d')))
			return HttpResponseRedirect("/integracion/censo/servicio/")

		form = ServicioForm(request.POST)
		if not form.is_valid():
			messages.info(request, form.errors)
			return HttpResponseRedirect("/integracion/censo/servicio/")

		form.save()

		return HttpResponseRedirect("/integracion/censo/servicio/?reload=%s" % (datetime.now()))
	
	record_report  = get_file_data()
	if record_report is None:
		return HttpResponseRedirect("/404/")

	context = {
		'services': get_services_from_file(record_report.filename, extras = False),
		'filtered': get_dict_from_data(record_report.filename),
		'alldata': get_valid_rows(record_report.filename),
		'list': Servicio.objects.all().order_by('fecha')
	}
	return render(request, 'censo_servicio.html', context)

def censo_paciente_detalle(request):
	context = {}
	_id = request.GET.get('censo_id', '-')
	
	if _id == '-':
		return HttpResponseRedirect("/404/")
	
	context['censo'] = Censo.objects.get(id = _id)
	# 
	# print(">>>>", context['censo'].salida_tipo)

	return render(request, 'censo_paciente_detalle.html', context)

def censo_delete(request):
	censo_id = request.GET.get('censo_id', '-')
	if censo_id == '-':
		return HttpResponseRedirect("/404/")
	
	censo_object = Censo.objects.get(id = censo_id)
	servicio = censo_object.servicio

	if censo_object.salida_tipo == '---':
		return HttpResponseRedirect("/404/")

	censo_object.delete()

	return HttpResponseRedirect("/integracion/censo/?servicio_id=%s" % servicio.id)

def censo_input_synced(request):
	censo_id = request.POST.get('censo_id', '-')
	if censo_id == '-':
		return HttpResponseRedirect("/404/")

	censo_object = Censo.objects.get(id = censo_id)
	servicio = censo_object.servicio
	val = request.POST.get("synced")
	
	if val == "on":
		censo_object.input_synced = True
	else:
		censo_object.input_synced = False
	
	censo_object.save()

	return HttpResponseRedirect("/integracion/censo/?servicio_id=%s" % servicio.id)

def censo_output_synced(request):
	censo_id = request.POST.get('censo_id', '-')
	if censo_id == '-':
		return HttpResponseRedirect("/404/")

	censo_object = Censo.objects.get(id = censo_id)
	servicio = censo_object.servicio
	
	val = request.POST.get("synced")
	
	if val == "on":
		censo_object.output_synced = True
	else:
		censo_object.output_synced = False

	censo_object.save()

	return HttpResponseRedirect("/integracion/censo/salidas/?servicio_id=%s" % (servicio.id))

def censo_servicio_synced(request):
	if request.method == "POST":
		servicio = Servicio.objects.get(id = request.POST.get("servicio_id"))
		val = request.POST.get("synced")
		
		if val == "on":
			servicio.synced = True
			servicio.save()
		else:
			servicio.synced = False
			servicio.save()
	return HttpResponseRedirect("/integracion/censo/servicio/")

def censo_salida(request):
	if request.method == "POST":
		censo = Censo.objects\
			.get(id = request.POST.get("censo_id"))
		
		if censo.has_gone():
			return HttpResponseRedirect(censo.get_link())
		
		POST = request.POST.copy()
		
		POST['salida'] = POST.get('salida', '-')
		if len(POST['salida']) <= 0:
			POST['salida'] = '-'
		
		form = CensoSalidaForm(POST, instance = censo)
		if not form.is_valid():
			messages.info(request, form.errors)
			return HttpResponseRedirect("/integracion/censo/salida/?censo_id=%s" % (censo.id))
			
		form.save()
		return HttpResponseRedirect(censo.get_link())

	
	record_report  = get_file_data()
	if record_report is None:
		return HttpResponseRedirect("/404/")

	context = {
		'services': get_services_from_file(record_report.filename, extras = False)
	}

	_id = request.GET.get('censo_id', '-')
	
	if _id == '-':
		return HttpResponseRedirect("/404/")
	
	context['censo'] = Censo.objects.get(id = _id)
	
	# context['outputs'] = context['censo'].get_outputs()
	if context['censo'].salida_tipo != '---':
		return HttpResponseRedirect(context['censo'].get_link())
	# if context['outputs'].exists():
	# 	return HttpResponseRedirect(context['censo'].get_link())
	
	return render(request, 'censo_salida.html', context)
