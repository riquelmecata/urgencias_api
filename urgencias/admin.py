from django.contrib import admin
# Asegúrate de importar TODOS tus modelos aquí 👇
from .models import Cargo, Usuario, Formulario, Evidencia, Historial

# Registros simples
admin.site.register(Cargo)
admin.site.register(Usuario)
admin.site.register(Evidencia)
admin.site.register(Historial)

# Registro "bonito" para el Formulario 
# (Así podrás ver el nombre del paciente y la fecha en la lista antes de borrar)
@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_formulario', 'fecha_envio_formulario', 'prioridad_formulario')
    search_fields = ('nombre_formulario',)