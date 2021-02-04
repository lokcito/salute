from django.contrib import admin
from .models import Neonato, SalaObservacion, TurnoMedico, Tercero
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class NeonatoResource(resources.ModelResource):
        class Meta:
                model = Neonato

@admin.register(Neonato)
class NeonatoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
        list_filter = (
                ('fecha', DateRangeFilter),
        )
        fields =['dato','fecha', ('sexo','tipo', 'reg'), ('dni','transf')]
        list_display = ('dato','fecha','sexo','tipo','dni','user','transf','reg')
        search_fields = ['dato','dni']
        list_editable = ("reg",)
        list_per_page = 12
        

@admin.register(SalaObservacion)
class SalaObservacionAdmin(admin.ModelAdmin):
        fields = [('ingreso','dni'),('apellido1','apellido2'),('nombre1','nombre2'),('edad','ambiente','cama'),('salida','estado')]
        list_display = ('ingreso','apellido1','apellido2','nombre1','cama')
        search_fields = ['dni', 'apellido1','apellido2','nombre1','nombre2']
        list_per_page = 9
        
@admin.register(TurnoMedico)
class TurnoMedicoAdmin(admin.ModelAdmin):
    fields = ['fecha','topico',('medico','turno')]
    list_display = ('fecha','topico','medico','turno')
    list_per_page = 9
    
class TerceroResource(resources.ModelResource):
        class Meta:
                model = Tercero
                                
@admin.register(Tercero)
class TerceroAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    fields = ['fecha',('dni','paciente','domicilio'),('edad','sexo','celular','profesion'),('condicion','observacion')]
    list_display = ('dni','fecha','paciente','domicilio','edad','sexo','celular','condicion')
    search_fields = ['dni','paciente']
    list_per_page = 12
    resources_class = TerceroResource

admin.site.disable_action('delete_selected')



