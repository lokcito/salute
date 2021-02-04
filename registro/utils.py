import requests
from pytz import timezone
from datetime import datetime
from datetime import datetime, time, timedelta

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

def scrapfile():
	s = requests.Session()
	response = s.post('http://172.20.0.210:8080/explotacionDatos/servlet/Index', data={
		"USER": "41713667",
		"PASS": "help778020",
		"upd": "index",
		"opt": "0",
		"Submit": "Ingresar"
	})
	#print(">>", response.status_code)
	#print("||>", response.text)
	response = s.post('http://172.20.0.210:8080/explotacionDatos/servlet/Index', data={
		"centroAsistencial": "307",
		"upd": "indexCas",
		"opt": "0",
		"USER": "41713667",
		"PASS": "help778020"
	})
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