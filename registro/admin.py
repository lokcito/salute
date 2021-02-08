from django.contrib import admin
from .models import Neonato, Censo, Paciente, Servicio, TurnoMedico, Tercero, Pagare
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

@admin.register(Pagare)
class PagareAdmin(admin.ModelAdmin):
    fields = [('fecha','pagare','contingencia'),('dni1','paciente'),('dni2','aval'),('domicilio','movil'),('obs')]
    list_display = ('fecha','pagare','contingencia','dni1','paciente','dni2','aval','domicilio','movil','obs')
    list_per_page = 10
        
@admin.register(Censo)
class CensoAdmin(admin.ModelAdmin):
        fields = [('ncama','adm'),('transferencia','alta'),('servicio')]
        list_display = ('paciente','ncama','adm','transferencia','alta','servicio')
        search_fields = ['paciente', 'servicio']
        list_per_page = 9

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
        class Meta:
                model = Paciente
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
        class Meta:
                model = Servicio

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



