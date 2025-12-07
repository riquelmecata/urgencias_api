from django.contrib import admin

from urgencias.models import Cargo, Usuario

class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_cargo']

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_usuario', 'apellido_usuario', 'email_usuario', 'cargo_usuario']

admin.site.register(Cargo, CargoAdmin)
admin.site.register(Usuario, UsuarioAdmin)