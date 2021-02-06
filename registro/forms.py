from django.forms import ModelForm
from registro.models import Servicio, Censo

# Create the form class.
class ServicioForm(ModelForm):
	class Meta:
		model = Servicio
		exclude = []

class CensoIngresoForm(ModelForm):
	class Meta:
		model = Censo
		exclude = []

class CensoSalidaForm(ModelForm):
	class Meta:
		model = Censo
		exclude = ['paciente', 
			'ncama', 
			'adm', 
			'transferencia', 
			'servicio']