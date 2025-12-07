from django.db import models

class Cargo(models.Model):
    nombre_cargo = models.TextField(max_length=100)

    def __str__(self):
        return str(self.nombre_cargo)

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, blank=True, null=True)
    apellido_usuario = models.CharField(max_length=100, blank=True, null=True) 
    email_usuario = models.EmailField(max_length=100, unique=True)
    password_usuario = models.TextField(max_length=20)
    cargo_usuario = models.ForeignKey(Cargo, on_delete=models.CASCADE)

class Formulario(models.Model):
    nombre_formulario = models.TextField(max_length=100)
    genero_formulario = models.TextField(max_length=20)
    edad_formulario = models.IntegerField()

    ant_formulario = models.TextField(max_length=200, blank=True, null=True)
    alergia_formulario = models.TextField(max_length=200, blank=True, null=True)

    motivo_formulario = models.TextField(null=True)

    presion_formulario = models.TextField(max_length=20, blank=True, null=True)
    pulso_formulario = models.TextField(max_length=20, blank=True, null=True)
    temperatura_formulario = models.TextField(max_length=20, blank=True, null=True)
    saturacion_formulario = models.TextField(max_length=20, blank=True, null=True)

    fecha_envio_formulario = models.DateTimeField(auto_now_add=True, null=True) 

    observaciones_formulario = models.TextField(blank=True, null=True)
    prioridad_formulario = models.TextField(max_length=20, blank=True, null=True)
    preparacion_formulario = models.TextField(max_length=20, blank=True, null=True)
    estado_formulario = models.TextField(max_length=20, default="Recibido")

    diagnostico_formulario = models.TextField(blank=True, null=True)
    tratamiento_formulario = models.TextField(blank=True, null=True)

    paramedico_formulario = models.TextField(max_length=100, blank=True, null=True)
    enfermera_formulario = models.TextField(max_length=100, blank=True, null=True)



class Evidencia(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    imagen = models.FileField(upload_to='evidencias/', null=True, blank=True)


class Historial(models.Model):
    descripcion_historial = models.TextField()
    tabla_afectada_historial = models.TextField(max_length=100)
    fecha_hora_historial = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tabla_afectada_historial} - {self.descripcion_historial[:50]}"





