from rest_framework import serializers
from .models import Cargo, Usuario, Formulario, Evidencia, Historial

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = "__all__"

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

class EvidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidencia
        fields = ['id', 'imagen']

class FormularioSerializer(serializers.ModelSerializer):
    imagenes = EvidenciaSerializer(source='evidencia_set', many=True, read_only=True)

    class Meta:
        model = Formulario
        fields = '__all__'


class HistorialSerializer(serializers.ModelSerializer):
    # expone explícitamente el id del usuario asociado
    usuario_id = serializers.IntegerField(read_only=True)
    nombre_usuario = serializers.CharField(source='usuario.nombre_usuario', read_only=True)
    apellido_usuario = serializers.CharField(source='usuario.apellido_usuario', read_only=True)
    fecha_hora_historial = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S', read_only=True)

    class Meta:
        model = Historial
        fields = '__all__'