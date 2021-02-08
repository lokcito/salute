import os.path
from os import path
import requests
from pytz import timezone
from datetime import datetime
from datetime import datetime, time, timedelta

def auth_essalud():
	s = requests.Session()
	response = s.post('http://sgss.essalud/sgss/servlet/hmain', data={
		"W0005_USECOD": "41713667",
		"W0005_CLAVE": "help778020",
		"_EventName":	"W0005EENTER.",
		"_EventGridId":	"",
		"_EventRowId":	"",
		"W0004_CMPPGM":	"hcabecera",
		"W0005_CMPPGM":	"hloginini",
		"W0005_USECOD":	"41713667",
		"W0005_CLAVE":	"help778020",
		"W0005BTNLOGIN":	"Login",
		"W0005_APENOMUSU":	"",
		"W0005_NEWCLAVE":	"",
		"W0005_RETYPECLAVE":	"",
		"W0005_PEREMAIL1":	"",
		"W0005_PERTEL1":	"",
		"W0005_PEREMAIL2":	"",
		"W0005_PERTEL2":	"",
		"W0005_NCENTROS":	"0",
		"W0005_NTBL":	"0",
		"W0005_NINT":	"0",
		"W0005_FLGCAM":	"0",
		"W0005_CUSER":	"",
		"W0005_FLGVIGPWR":	"0",
		"W0005_PAGINTPERNUM":	"9",
		"W0005_PAGDIASACCCAN":	"90",
		"W0007_CMPPGM":	"hpie",
		"sCallerURL":	""		
	})
	return s
	# response = s.post('http://172.20.0.210:8080/explotacionDatos/servlet/Index', data={
	# 	"centroAsistencial": "307",
	# 	"upd": "indexCas",
	# 	"opt": "0",
	# 	"USER": "41713667",
	# 	"PASS": "help778020"
	# })
	# return s

def scrap_services():
	_now = datetime_now()

	local_filename = "./tmp/servicios-%s.txt" % (_now.strftime('%Y-%m-%d-%H'))	

	if path.exists(local_filename):
		pass
	else:
		s = auth_essalud()
		response = s.post("http://sgss.essalud/sgss/servlet/hmainmenu", {
			"_EventName": "E'OTORGAMENU'.0009",
			"_EventGridId": "",
			"_EventRowId": "",
			"MPW0004_CMPPGM": "hcabecera",
			"MPW0005_CMPPGM": "hloginmenu",
			"GXimgMPW0005_IMGFLG": "/images/btn_previous.gif",
			"MPW0005_NTBL": "0",
			"MPW0005_TRAGXENC": "TtgYT39IXXXGV9Mw8YbUnQ==",
			"GXimg_PGMICO_0001": "/images/i_citas.jpg",
			"_PGMCOD_0001": "C0000000000",
			"_PGMORD_0001": "0",
			"GXimg_PGMICO_0002": "/images/i_consexterna.jpg",
			"_PGMCOD_0002": "E0000000000",
			"_PGMORD_0002": "0",
			"GXimg_PGMICO_0003": "/images/i_emergencia.jpg",
			"_PGMCOD_0003": "G0000000000",
			"_PGMORD_0003": "0",
			"GXimg_PGMICO_0004": "/images/i_hospital.jpg",
			"_PGMCOD_0004": "H0000000000",
			"_PGMORD_0004": "0",
			"GXimg_PGMICO_0005": "/images/i_quirurgico.jpg",
			"_PGMCOD_0005": "I0000000000",
			"_PGMORD_0005": "0",
			"GXimg_PGMICO_0006": "/images/i_farmaciadep.jpg",
			"_PGMCOD_0006": "T0000000000",
			"_PGMORD_0006": "0",
			"GXimg_PGMICO_0007": "/images/i_ayudadx.jpg",
			"_PGMCOD_0007": "U0000000000",
			"_PGMORD_0007": "0",
			"GXimg_PGMICO_0008": "/images/i_reportes.jpg",
			"_PGMCOD_0008": "V0000000000",
			"_PGMORD_0008": "1",
			"GXimg_PGMICO_0009": "/images/i_tablas.jpg",
			"_PGMCOD_0009": "X0000000000",
			"_PGMORD_0009": "0",
			"GXimg_PGMICO_0010": "/images/i_liquidacion.jpg",
			"_PGMCOD_0010": "Y0000000000",
			"_PGMORD_0010": "0",
			"GXimg_PGMICO_0011": "/images/i_seguridad.jpg",
			"_PGMCOD_0011": "Z0000000000",
			"_PGMORD_0011": "0",
			"MPW0008_CMPPGM": "hpie",
			"nRC_Grd_sistemas": "11",
			"sCallerURL": "",
		})
		lines = response.text.split(";")
		new_path = None
		_new = None
		for x in lines:
			if "Estac.de Enfermeras" in x:
				new_path = x.split("','")
				if len(new_path) == 2:
					_new = "http://sgss.essalud/sgss/servlet/%s" % (new_path[1][0:-2])
					break
		if _new is None:
			return []

		r = s.get(_new, stream=True)

		with open(local_filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024):
				f.write(chunk)

	f = open(local_filename, encoding="utf8", mode = 'r+')
	lines = [line for line in f.readlines()]
	f.close()

	all_content = "".join(lines)

	from lxml import html
	soup = html.fromstring(all_content)
	__list = soup.xpath("//select[@name='_SERVHOSCOD']/option/text()")
	_list = []
	for uu in __list:
		if 'Seleccione' in uu:
			continue
		_list.append(uu)


	return _list

def scrap_people(_dni):
	s = auth_essalud()
	response = s.post("http://sgss.essalud/sgss/servlet/hbuspacemer", {
		"_EventName": "E'BUSDOCIDE'.",
		"_EventGridId": "",
		"_EventRowId": "",
		"MPW0004_CMPPGM": "hcabecera",
		"MPW0005_CMPPGM": "hloginmenu",
		"GXimgMPW0005_IMGFLG": "/images/btn_previous.gif",
		"MPW0005_NTBL": "0",
		"MPW0005_TRAGXENC": "uvoS8xpi9ekBw0sTvO5eaQ==",
		"_ORICENASICOD": "1",
		"_CENASICOD": "307",
		"_AREHOSCOD": "02",
		"_EMECOD": "01",
		"_FLAGTIPO": "0",
		"_NCASO": "0",
		"_PERTIPDOCIDENCOD": "1",
		"_PERDOCIDENNUM": _dni,
		"_ATETRIANOBUS": "2021",
		"_ATETRINUMBUS": "0",
		"_PERAPEPATDES": "",
		"_PERAPEMATDES": "",
		"_PERPRINOMDES": "",
		"_PERSEGNOMDES": "",
		"W0037": "",
		"MPW0008_CMPPGM": "hpie",
		"sCallerURL": "http://sgss.essalud/sgss/servlet/hmainmenu",
		"_PGMDESC": "Busca Paciente en Admision Emergencia",
	})
	
	from lxml import html
	soup = html.fromstring(response.content)
	ap_paterno = soup.xpath('//span[@id="span_W0037_DGATAPA_0001"]/text()')
	ap_materno = soup.xpath('//span[@id="span_W0037_DGATAMA_0001"]/text()')
	nombre_one = soup.xpath('//span[@id="span_W0037_DGATPNO_0001"]/text()')
	nombre_two = soup.xpath('//span[@id="span_W0037_DGATSNO_0001"]/text()')	

	if len(ap_paterno) > 0 and len(ap_materno) > 0 and \
		len(nombre_one) > 0 and len(nombre_two) > 0:
		return {
			"dni": _dni,
			"nombres": "%s %s" % (nombre_one[0], nombre_two[0]),
			"apellidos": "%s %s" % (ap_paterno[0], ap_materno[0]),
		}

	if len(ap_paterno) > 0 and len(ap_materno) > 0 and \
		len(nombre_one) > 0:
		return {
			"dni": _dni,
			"nombres": "%s" % (nombre_one[0]),
			"apellidos": "%s %s" % (ap_paterno[0], ap_materno[0]),
		}		
		
	return None	

def paciente_get_or_create(_dni):
	from registro.models import Paciente
	from datetime import datetime

	o = Paciente.objects.filter(dni = _dni).first()
	if o is None:
		_data = scrap_people(_dni)

		pa = Paciente(dni = _dni, 
			nombre = _data["nombres"],
			apellido = _data["apellidos"])
		pa.ingreso = datetime.now()
		pa.save()
		return pa
	return o
def get_valid_rows(filename):
	f = open(filename, encoding="utf8", mode = 'r+')
	lines = [line for line in f.readlines()]
	f.close()

	rr = []
	ii = 0
	for x in lines[1:]:
		cols = x.split("|")
		if len(cols) != 13:
			continue
		if cols[7] in ["OCUPADA", "DISPONIBLE"]:
			cols.append(ii)
			rr.append(cols)
			ii += 1;
	return rr

def get_services(_filename):
	ss = []
	for x in get_valid_rows(_filename):
		ss.append(x[3])
	mylist = list(dict.fromkeys(ss))
	return mylist

def get_station_from_list(_list):
	ss = []
	for x in _list:
		ss.append(x[4])
	mylist = list(dict.fromkeys(ss))
	return mylist

def get_analytics_from_list(_list):
	dd = list(filter(lambda x: x[7] == "DISPONIBLE", _list))
	d = len(dd)
	oo = list(filter(lambda x: x[7] == "OCUPADA", _list))
	o = len(oo)
	t = len(_list)
	ss = {
		"available": d,
		'amore': ",".join(["%s" % x[13] for x in dd]),
		'unable': o,
		'umore':  ",".join(["%s" % x[13] for x in oo]),
		'total': t,
		'tmore':  ",".join(["%s" % x[13] for x in _list]),
	}
	return ss
	

def get_dict_from_list(_all, _list):
	st = {}
	for s in _list:
		_all = list(filter(lambda x: x[4] == s, _all))
		st[s] = get_analytics_from_list(_all)
	return st


def get_list_from_data_vs_estacion(_all, estacion_list):
	st = []
	for s in estacion_list:
		_tmpall = list(filter(lambda x: x[4] == s, _all))
		st.append({
			'text': s,
			'data': get_analytics_from_list(_tmpall)

			})
	return st

def get_dict_from_data(_filename):
	md = {}
	_rows = get_valid_rows(_filename)
	for s in get_services(_filename):
		
		# md[s] = map(lambda x: 'lower' if x[3] == s else 'higher', _rows)
		md[s] = {}
		_all = list(filter(lambda x: x[3] == s, _rows))
		__all = get_station_from_list(_all)
		md[s]['Estaciones'] = get_list_from_data_vs_estacion(_all, __all)
	return md

		# print(md[s]['stations'])
#
#print(get_dict_from_data())
# print(get_services())


def datetime_now():
	return datetime.now(timezone('America/Lima'))

def get_file_data(force = False):
	from registro.models import FileDataReport

	_now = datetime_now()
	#print("aaa", _now)
	o = FileDataReport.objects.all().order_by('-id')
	current_file = None
	if not o.exists():
		scrapfile()
		current_file = FileDataReport.objects.all().order_by('-id').first()
	else:
		if force:
			scrapfile()
			current_file = FileDataReport.objects.all().order_by('-id').first()			
		else:
			#_now = _now + timedelta(minutes = 10)
			#print("mas 10", _now)
			date = o.first().get_fecha() + timedelta(minutes = 10)

			#print("fecha record0", date)
			if date < _now:
				scrapfile()
				current_file = FileDataReport.objects.all().order_by('-id').first()
			else:
				current_file = o.first()

	return current_file



def auth_explota():
	s = requests.Session()
	response = s.post('http://172.20.0.210:8080/explotacionDatos/servlet/Index', data={
		"USER": "41713667",
		"PASS": "help778020",
		"upd": "index",
		"opt": "0",
		"Submit": "Ingresar"
	})
	response = s.post('http://172.20.0.210:8080/explotacionDatos/servlet/Index', data={
		"centroAsistencial": "307",
		"upd": "indexCas",
		"opt": "0",
		"USER": "41713667",
		"PASS": "help778020"
	})
	return s


def scrapfile():
	s = auth_explota()
	#print(">>", response.status_code)
	#print("||>", response.text)
	#print(">>>", response.status_code)
	#print("||>", response.text)
	response = s.post('http://172.20.0.210:8080/explotacionDatos/servlet/CtrlControl?opt=hospitalCama_1_xls', {
		"area": "00",
		"servicio": "00",
		"estadoCama": "00",
		"formatoArchivo": "xls",
		"CAS": "307",
		"ORIGEN": "1"
	})

	excel_path = response.text[6:]
	last_route = "http://172.20.0.210:8080/explotacionDatos/servlet/CtrlControl?opt=hospitalCama_1_xls_descarga&fn=%s" % (excel_path)

	response = s.post(last_route, {
		"area": "00",
		"servicio": "00",
		"estadoCama": "00",
		"formatoArchivo": "xls",
		"CAS": "307",
		"ORIGEN": "1"
	})

	_now = datetime_now()
	filename = "./tmp/%s.txt" % (_now.strftime('%Y-%m-%d-%H-%M-%S'))
	with open(filename, 'wb') as f:
		f.write(response.content)		

		from registro.models import FileDataReport
		FileDataReport.create(filename)
	#print(">>>>", response.status_code)