from django.db import models
from datetime import datetime
from django.utils import timezone
import math
from django.db.models import IntegerField, Model
from django_userforeignkey.models.fields import UserForeignKey
#from django.contrib.auth.models import user


# Create your models here.

class Neonato(models.Model):
	dato = models.CharField(max_length=100,verbose_name='Datos del R.N.',help_text='Apellido Paterno  Apellido Materno  RN')
	fecha = models.DateTimeField(default=datetime.now, blank=True, verbose_name='Fecha y Hora Nacimiento')
	sexo = models.CharField(max_length=20, choices=(('Masculino','Masculino'),('Femenino','Femenino')))
	tipo = models.CharField(max_length=20, verbose_name='Tipo - Parto',choices=(('Natural','Natural'),('Cesarea','Cesarea')))
	dni = models.CharField(max_length=8,verbose_name='DNI - Madre o Tit.')
	reg = models.BooleanField(default=False, verbose_name='Registrado', help_text='Registrado-Marcara solo en Modulo cuando Neonato es Hospitalizado')
	user = UserForeignKey(auto_user_add=True, verbose_name='Usuario')
	transf = models.CharField(max_length=20, verbose_name='Transferir.',choices=(('Ucin','Ucin'),('InterMedio - 1','InterMedio - 1'),('InterMedio - 2','InterMedio - 2')), blank=True)

	def __str__(self):
		return self.dato

	def save(self, *args, **kwargs):
		self.dato = self.dato.upper()
		super(Neonato, self).save(*args, kwargs)

class TurnoMedico(models.Model):
	fecha = models.DateField(default=timezone.now, verbose_name='FECHA')
	topico = models.CharField(max_length=40, choices=(('JEFE DE GUARDIA','JEFE DE GUARDIA'),('SALA OBSERVACION','SALA OBSERVACION'),('MEDICINA 1','MEDICINA 1'),('MEDICINA 2','MEDICINA 2'),('PEDIATRIA','PEDIATRIA'),
	('CIRUGIA','CIRUGIA'),('GINEGOLOGIA','GINECOLOGIA'),('TRAUMATOLOGIA','TRAUMATOLOGIA'),('TRIAJE','TRIAJE')))
	medico = models.CharField(max_length=40)
	turno = models.CharField(max_length=40, choices=(('GUARDIA DIURNA','GUARDIA DIURNA'),('GUARDIA NOCTURNA','GUARDIA NOCTURNA')), blank=True)

	def __str__(self):
		return self.topico

	def save(self, *args, **kwargs):
		self.topico = self.topico.upper()
		self.medico = self.medico.upper()
		super(TurnoMedico, self).save(*args, kwargs)

class Tercero(models.Model):
	dni = models.CharField(max_length=8, verbose_name='D.N.I.')
	fecha = models.DateTimeField(default=datetime.now, verbose_name='Registro')
	paciente = models.CharField(max_length=70, verbose_name='Apellidos y Nombres')
	domicilio = models.CharField(max_length=60, verbose_name='Direccion')
	edad = models.PositiveSmallIntegerField(default = 1)
	sexo = models.CharField(max_length=20, choices=(('MASCULINO','MASCULINO'),('FEMENINO','FEMENINO')))
	celular = models.CharField(max_length=9, verbose_name='Telefono Movil', help_text="Numero de Contacto")
	profesion = models.CharField(max_length=30, choices=(('BOMBERO','BOMBERO'),('POLICIA','POLICIA'),('PERSONAL DE SALUD','PERSONAL DE SALUD'),('OTRAS PROFESIONES','OTRAS PROFESIONES')))
	condicion = models.CharField(max_length=30, choices=(('TERCERO','TERCERO'),('SEGURO NO VIGENTE','SEGURO NO VIGENTE')))
	observacion = models.TextField(max_length=100, help_text="observaciones adicionales")

	def __str__(self):
		return self.paciente + ' ' + self.celular 

	def save(self, *args, **kwargs):
		self.paciente = self.paciente.upper()
		self.domicilio = self.domicilio.upper()
		self.observacion = self.observacion.upper()
		super(Tercero, self).save(*args, kwargs)

class Paciente(models.Model):
	ingreso = models.DateTimeField(default=datetime.now, blank=True, verbose_name='Fecha y Hora Ingreso')
	dni = models.CharField(max_length=8, verbose_name='D.N.I.')
	nombre = models.CharField(max_length=35, verbose_name='Nombre', blank=True)
	apellido = models.CharField(max_length=35, verbose_name='Apellidos', blank=True)
	
	def __str__(self):
		return self.dni

	def text(self):
		return "%s %s" % (self.nombre, self.apellido)

	def save(self, *args, **kwargs):
		self.nombre = self.nombre.upper()
		self.apellido = self.apellido.upper()
		super(Paciente, self).save(*args, kwargs)

class Servicio(models.Model):
	nombre = models.CharField(max_length=250)
	estacion = models.CharField(max_length=250)
	ncamas = models.IntegerField()
	fecha = models.DateTimeField(default=datetime.now, blank=True, verbose_name='Fecha de Registro')

class Censo(models.Model):
	paciente = models.ForeignKey(Paciente, 
		on_delete=models.CASCADE)
	ncama = IntegerField()
	adm = models.BooleanField(default=False)
	transferencia = models.CharField(max_length=250)
	gone = models.BooleanField(default=False)
	alta = models.BooleanField(default=False)
	servicio = models.ForeignKey(Servicio, 
		on_delete=models.CASCADE)
	usuario = UserForeignKey(auto_user_add=True, 
		verbose_name='Usuario')
	salida = models.CharField(max_length=250, 
		default = '-')
	
	def get_alta_text(self):
		return 'Si' if self.alta else 'No'
	
	def get_defuncion_text(self):
		return 'No' if self.alta else 'Si'
		
	
	def get_move(self):
		return '/integracion/censo/salida/?censo_id=%s' % (self.id)
	
	def get_link(self):
		return '/integracion/censo/paciente/detalle/?censo_id=%s' % (self.id)

	def get_adm_text(self):
		return 'Si' if self.adm else 'No'

	# def get_outputs(self):
	# 	return Censo.objects.filter(parent = self)

class Pagare(models.Model):
	fecha = models.DateField(default=datetime.now, blank=True, verbose_name='Fecha')
	pagare = models.CharField(max_length=7, verbose_name='N° de Pagare')
	contingencia = models.CharField(max_length=30, verbose_name='Contingencia',choices=(('NO ACREDITADO','NO ACREDITADO'),('AGRESION POR TERCEROS','AGRESION POR TERCEROS'),('ACCIDENTE DE TRANSITO','ACCIDENTE DE TRANSITO'),
	('ACCIDENTE DE MOTO','ACCIDENTE DE MOTO'),('PARTICULAR','PARTICULAR'),('INTENTO DE SUICIDIO','INTENTO DE SUICIDIO')))
	dni1 = models.CharField(max_length=8, verbose_name='D.N.I.')
	paciente = models.CharField(max_length=35, verbose_name='Datos del Paciente')
	dni2 = models.CharField(max_length=8, verbose_name='D.N.I')
	aval = models.CharField(max_length=40, verbose_name='Datos del Aval')
	domicilio = models.CharField(max_length=35, verbose_name='Domicilio')
	movil = models.CharField(max_length=9, verbose_name='Telefono / Movil')
	obs = models.CharField(max_length=200, verbose_name= 'Deposito/Garantia')
	#user = UserForeignKey(auto_user_add=True, verbose_name='Responsable')

	def __str__(self):
		return self.pagare

	def save(self, *args, **kwargs):
		self.paciente= self.paciente.upper()
		self.aval = self.aval.upper()
		self.domicilio = self.domicilio.upper()
		self.obs = self.obs.upper()
		super(Pagare, self).save(*args, kwargs)

class FileDataReport(models.Model):
	filename = models.CharField(max_length=250, verbose_name='Filename')
	fecha = models.DateTimeField(verbose_name='Registro')
	
	def get_fecha(self):
		from pytz import timezone as timezonex
		return self.fecha.\
			astimezone(
				timezonex("America/Lima"))		

	def get_fecha_text(self):
		from pytz import timezone as timezonex
		return self.fecha.\
			astimezone(
				timezonex("America/Lima"))\
				.strftime("%Y-%m-%d %H:%M:%S")

	@staticmethod
	def create(_filename):
		from registro.utils import datetime_now
		g = FileDataReport()
		g.filename = _filename
		g.fecha = datetime_now()
		g.save()