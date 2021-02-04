from django.db import models
from datetime import datetime
from django.utils import timezone
import math
from django_userforeignkey.models.fields import UserForeignKey
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

class SalaObservacion(models.Model):
	ingreso = models.DateTimeField(default=datetime.now, blank=True, verbose_name='Fecha y Hora Ingreso')
	dni = models.CharField(max_length=8, verbose_name='D.N.I.')
	apellido1 = models.CharField(max_length=35, verbose_name='Apellido Paterno', blank=True)
	apellido2 = models.CharField(max_length=35, verbose_name='Apellido Materno', blank=True)
	nombre1 = models.CharField(max_length=35, verbose_name='Primer Nombre', blank=True)
	nombre2 = models.CharField(max_length=35, verbose_name='Segundo Nombre', blank=True)
	edad = models.CharField(max_length=3, verbose_name='Edad', blank=True)
	historia =models.CharField(max_length=8, verbose_name='Hist. Clinica', blank=True)
	ambiente = models.CharField(max_length=30, choices=(
	('OBS. ADULTO','OBS. ADULTO'),('OBS. PEDIATRICO','OBS. PEDIATRICO')))
	cama = models.CharField(max_length=30, verbose_name='Cama', choices=(
	('CAMA-01','CAMA-01'),('CAMA-02','CAMA-02'),('CAMA-03','CAMA-03'),('CAMA-04','CAMA-04'),('CAMA-05','CAMA-05'),('CAMA-06','CAMA-06'),
	('CAMA-07','CAMA-07'),('CAMA-08','CAMA-08'),('CAMA-09','CAMA-09'),('CAMA-10','CAMA-10'),('CAMA-11','CAMA-11'),('CAMA-12','CAMA-12'),
	('CAMA-13','CAMA-13'),('CAMA-14','CAMA-14'),('CAMA-15','CAMA-15'),('CAMA-16','CAMA-16'),('CAMA-17','CAMA-17'),('CAMA-18','CAMA-18'),
	('CAMA-19','CAMA-19'),('CAMA-20','CAMA-20'),('CAMA-21','CAMA-21'),('CAMA-22','CAMA-22'),('CAMA-23','CAMA-23'),('CAMA-24','CAMA-24'),
	('CAMA-25','CAMA-25'),('CAMA-26','CAMA-26')))
	salida = models.DateTimeField(default=datetime.now, verbose_name='Fecha y Hora Alta', blank=True)
	estancia_hora = models.DecimalField(max_digits=5, decimal_places=2)
	estado = models.CharField(max_length=30, choices=(
		('HOSPITALIZADO','HOSPITALIZADO'),('TRANSF. INTERNA','TRANSF. INTERNA'),('TRANSF. EXTERNA','TRANSF. EXTERNA'),('ALTA','ALTA'),('MORGE','MORGE')))

	def __str__(self):
		return self.dni
	def estancia_hora(self):
                return math.ceil((self.salida - self.ingreso).total_seconds() / 3600)

	def save(self, *args, **kwargs):
		self.apellido1 = self.apellido1.upper()
		self.apellido2 = self.apellido2.upper()
		self.nombre1 = self.nombre1.upper()
		self.nombre2 = self.nombre2.upper()
		super(SalaObservacion, self).save(*args, kwargs)

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