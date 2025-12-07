from django.shortcuts import render
from django.http import JsonResponse

from urgencias.models import Formulario, Evidencia, Usuario, Historial
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from urgencias.serializers import FormularioSerializer, HistorialSerializer

def _get_user_id_from_request(request):
    """Intentar obtener user id de varias fuentes: body JSON, form-data, query params, headers o request.user."""
    # 1) request.data (JSON / form-data manejado por DRF)
    try:
        data = request.data if hasattr(request, 'data') else {}
        # request.data puede no ser dict; intentar obtener claves comunes
        for key in ('user_id', 'usuario_id', 'user', 'id'):
            if isinstance(data, dict) and key in data and data[key] not in (None, ''):
                try:
                    return int(data[key])
                except Exception:
                    pass
            # QueryDict (p.ej. form-data) tiene getlist/get
            try:
                val = data.get(key)
                if val not in (None, ''):
                    return int(val)
            except Exception:
                pass
    except Exception:
        pass

    # 2) request.POST (por si DRF no llenó request.data)
    try:
        post = request.POST
        for key in ('user_id', 'usuario_id', 'user', 'id'):
            val = post.get(key)
            if val not in (None, ''):
                try:
                    return int(val)
                except Exception:
                    pass
    except Exception:
        pass

    # 3) query params
    try:
        for key in ('user_id', 'usuario_id', 'user', 'id'):
            val = request.query_params.get(key)
            if val not in (None, ''):
                try:
                    return int(val)
                except Exception:
                    pass
    except Exception:
        pass

    # 4) cabeceras comunes
    try:
        val = request.META.get('HTTP_X_USER_ID') or request.META.get('X-USER-ID') or request.META.get('HTTP_USER_ID')
        if val not in (None, ''):
            try:
                return int(val)
            except Exception:
                pass
    except Exception:
        pass

    # 5) si hay autenticación, usar request.user.id
    try:
        if hasattr(request, 'user') and request.user and getattr(request.user, 'id', None):
            return int(request.user.id)
    except Exception:
        pass

    return None

# def obtenerUsuarios(request):
#     usu = Usuario.objects.all()
#     datos = { "usu" : list(usu.values('id', 'email_usuario', 'cargo_usuario'))}
#     return JsonResponse(datos)

# def obtenerFormularios(request):
#     form = Formulario.objects.all()
#     datos = { "form" : list(form.values('id', 'nombre_formulario', 'genero_formulario', 'edad_formulario', 'ant_formulario', 'alergia_formulario', 'motivo_formulario', 'presion_formulario', 'pulso_formulario', 'temperatura_formulario', 'saturacion_formulario', 'fecha_envio_formulario', 'observaciones_formulario', 'prioridad_formulario', 'preparacion_formulario', 'diagnostico_formulario', 'tratamiento_formulario'))}
#     return JsonResponse(datos)

@api_view(['POST'])
def formularios_create(request):
    # Crear formulario sin imágenes primero
    ser = FormularioSerializer(data=request.data, partial=True)

    if ser.is_valid():
        formulario = ser.save()   # ← ya tenemos el ID del formulario

        # Guardar imágenes si vienen
        if 'imagenes' in request.FILES:
            for img in request.FILES.getlist('imagenes'):
                Evidencia.objects.create(
                    formulario=formulario,
                    imagen=img
                )

        # Registrar en historial
        usuario_id = _get_user_id_from_request(request)
        descripcion = f"Creación de formulario"
        Historial.objects.create(descripcion_historial=descripcion, tabla_afectada_historial='Formulario', usuario_id=usuario_id)

        return Response(ser.data, status=status.HTTP_201_CREATED)

    return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def formularios_list(request):
    if request.method == 'GET':
        form = Formulario.objects.all()
        ser = FormularioSerializer(form, many=True)
        return Response(ser.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def formulario_detail(request, id):
    try:
        form = Formulario.objects.get(id = id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        ser = FormularioSerializer(form)
        return Response(ser.data)
    
    if request.method == 'PUT':
        ser = FormularioSerializer(form, data=request.data, partial=True)
        if ser.is_valid():
            instance = ser.save()

            usuario_id = _get_user_id_from_request(request)
            descripcion = f"Actualización formulario"
            Historial.objects.create(descripcion_historial=descripcion, tabla_afectada_historial='Formulario', usuario_id=usuario_id)

            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        usuario_id = _get_user_id_from_request(request)

        descripcion = f"Eliminación formulario"
        Historial.objects.create(descripcion_historial=descripcion, tabla_afectada_historial='Formulario', usuario_id=usuario_id)

        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST'])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        usuario = Usuario.objects.get(email_usuario=email)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=400)

    # ⚠️ Si tus contraseñas NO están encriptadas, usa esto:
    if usuario.password_usuario != password:
        return Response({"error": "Contraseña incorrecta"}, status=400)

    # Registrar inicio de sesión en historial
    try:
        descripcion = f"Inicio de sesión usuario"
        Historial.objects.create(descripcion_historial=descripcion, tabla_afectada_historial='', usuario_id=usuario.id)
    except Exception:
        # no bloquear login si falla el registro del historial
        pass

    # Respuesta con datos del usuario
    return Response({
        "id": usuario.id,
        "nombre": usuario.nombre_usuario,
        "apellido": usuario.apellido_usuario,
        "email": usuario.email_usuario,
        "cargo": usuario.cargo_usuario.nombre_cargo
    }, status=200)


@api_view(['GET'])
def historial(request):
    """Vista pública que devuelve el historial. La validación de admin
    debe hacerse desde el front-end. Opcionalmente admite filtros:
    ?usuario_id=, ?tabla=, ?desde=<ISO_DATETIME>, ?hasta=<ISO_DATETIME>
    """
    entradas = Historial.objects.all().order_by('-fecha_hora_historial')

    usuario_id = request.query_params.get('usuario_id')
    tabla = request.query_params.get('tabla')
    desde = request.query_params.get('desde')
    hasta = request.query_params.get('hasta')

    if usuario_id:
        try:
            entradas = entradas.filter(usuario_id=int(usuario_id))
        except Exception:
            pass

    if tabla:
        entradas = entradas.filter(tabla_afectada_historial__iexact=tabla)

    if desde or hasta:
        from django.utils.dateparse import parse_datetime
        if desde:
            dt_desde = parse_datetime(desde)
            if dt_desde:
                entradas = entradas.filter(fecha_hora_historial__gte=dt_desde)
        if hasta:
            dt_hasta = parse_datetime(hasta)
            if dt_hasta:
                entradas = entradas.filter(fecha_hora_historial__lte=dt_hasta)

    ser = HistorialSerializer(entradas, many=True)
    return Response(ser.data)

@api_view(['POST'])
def logout(request):
    """
    Registra el cierre de sesión en Historial.
    Usa el helper para obtener user id desde body/query/headers/request.user.
    """
    usuario_id = _get_user_id_from_request(request)

    descripcion = f"Cierre de sesión usuario" if usuario_id else "Cierre de sesión (usuario desconocido)"
    try:
        Historial.objects.create(descripcion_historial=descripcion, tabla_afectada_historial=' ', usuario_id=usuario_id)
    except Exception:
        pass

    return Response({"detail": "Logout registrado"}, status=200)
