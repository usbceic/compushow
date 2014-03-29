from django.shortcuts     import render_to_response, get_object_or_404, redirect
from votaciones.models    import *
from django.contrib.auth.models import User
from django.db.models     import *
from django.template      import RequestContext
from django.core.urlresolvers       import reverse
from django.contrib.auth.decorators import login_required
from compushow.settings import *
from django.db.models import Count

from django.http import Http404,  HttpResponse
from ast         import literal_eval
from datetime    import datetime
from decimal     import Decimal
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth         import authenticate, login, logout

import string;


def diccionario_base(diccionario, request):
    """ Informacion necesaria para el template base """
    EdicionActual = Edicion.objects.get(activa = True)
    return dict(diccionario, **{'direccion'   : request.path,
                                'hay_usuario' : request.user.is_authenticated(),
                                'usuario'     : request.user,
                                'estado'      : EdicionActual.etapa,
                               })

def home(request):
    return render_to_response('votaciones/home/index.html',
                              diccionario_base({}, request),
                              context_instance=RequestContext(request),
                              )

def info(request):
    return render_to_response('votaciones/informacion/index.html',
                              diccionario_base({}, request),
                              context_instance=RequestContext(request),
                              )


def pagina_login(request):
    next = '/'
    msg = None
    if(request.GET.__contains__('next')): next = request.GET['next']
    if(request.GET.__contains__('msg')):
        msg_id = request.GET['msg']
        if msg_id == "0":
            msg = "Carnet o contrasena incorrecta"
        elif msg_id == "1":
            msg = "El Carnet no esta en la base de datos de estudiantes de computacion, comuniquese con nosotros para resolver el problema"
        elif msg_id == "2":
            msg = "El carnet ingresado ya esta siendo usado, verifique si ya esta inscrito o comuniquese con nosotros"
        else:
            msg == "error "+str(msg_id)
    
    return render_to_response('votaciones/login/index.html',
                              diccionario_base({'next': next, 'msg' : msg}, request),
                              context_instance=RequestContext(request),
                              )

def signup_do(request):
    try:
        carnet = Carnet.objects.get(pk=request.POST['username'])

        if(carnet.usado):
            response = redirect(reverse('votaciones.views.pagina_login'))
            response['Location'] += '?next='+str(request.POST['next'])+'&msg=2'
            return response
        else:
            carnet.usado = True
            carnet.save()
        
        username = carnet.numero
        password = request.POST['password']

        user = User.objects.create_user(username, request.POST['Email'], password)
        nombres = carnet.nombre.split(' ')
        first = int(len(nombres)/2)
        user.first_name = ' '.join(nombres[:first])
        user.last_name  = ' '.join(nombres[first:])
        user.save()

        login(request, authenticate(username=user.username, password=password))
        return redirect(request.POST['next'])
    except ObjectDoesNotExist:
        response = redirect(reverse('votaciones.views.pagina_login'))
        response['Location'] += '?next='+str(request.POST['next'])+'&msg=1'
        return response
    



def login_do(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            print "holaaaa"
            print request.POST['next']
            return redirect(request.POST['next'])

    response = redirect(reverse('votaciones.views.pagina_login'))
    response['Location'] += '?next='+str(request.POST['next'])+'&msg=0'
    return response

def logout_do(request):
    logout(request)
    next = '/'
    if(request.GET.__contains__('next')): next = request.GET['next']
    return redirect(next)

def informacion(request):
    return render_to_response('votaciones/home/index.html',
                              diccionario_base({}, request),
                              context_instance=RequestContext(request),
                              )

def ediciones(request):
    return render_to_response('votaciones/home/index.html',
                              diccionario_base({}, request),
                              context_instance=RequestContext(request),
                              )

def nominaciones(request):
    categorias = Categoria.objects.filter(edicion = Edicion.actual())

    #Votos del Usuario
    votos        = VotoNominacion.objects.select_related('nominacion', 'nominacion__categoria','media').filter(user_id=request.user.pk).order_by('nominacion__categoria__nombre')
    fotos        = Foto.objects.select_related('media').filter(media__in=votos.values('media'))
    videos       = Video.objects.select_related('media').filter(media__in=votos.values('media'))
    #Nominados a las nominaciones
    nominados    = Nominado.objects.filter(nominacion__in=votos.values('nominacion'))

    msg = None
    if(request.GET.__contains__('msg')):
        msg_id = request.GET['msg']
        if msg_id == "0":
            msg = "No puedes proponer dos veces la misma nominacion"

    return render_to_response('votaciones/nominar/index.html',
                              diccionario_base(
                                    {
                                    'votos'       :votos,
                                    'nominados'   :nominados,
                                    'categorias'  :categorias,
                                    'fotos'       :fotos,
                                    'videos'      :videos,
                                    'msg'         :msg,
                                    }, request),
                              context_instance=RequestContext(request),
                              )

@login_required(login_url='login')
def borrar_voto_nominacion(request):
    respuesta = None
    voto_id = int(request.POST['id'])
    
    try:
        voto = VotoNominacion.objects.select_related('media').filter(user_id=request.user.pk).get(pk=voto_id)
        voto.delete()
        respuesta = '1'
    except:
        respuesta = '0'

    return HttpResponse(respuesta, mimetype='text/plain')
    

@login_required(login_url='login')
def nominar_do(request):
    numero_nominados = int(request.POST["nominados"])
    numero_videos = int(request.POST["videos"])

    nominados = []
    user_id = request.user.id

    ###Preparecion de la Nominacion###:
    #Categoria de la nomiacin:
    categoria    = Categoria.objects.get(pk = request.POST["categoria"])

    #Lista de nominaciones en la categoria
    nominaciones = Nominacion.objects.select_related('nominado_set').filter(categoria=categoria)

    nominacion = None;

    #Construyendo lista de nominados
    for i in range(numero_nominados):
        nombre_nominado = request.POST["nominado"+str(i)]
        nominados.append(nombre_nominado)
    

    #Se verifica si ya hay una nominacion con el mismo conjunto de nominados en cuyo caso es la misma nominacion
    #Ordeno la lista por nombre para comparacion lineal
    nominados.sort()
    for nominacion_db in nominaciones:
        nominados_set = nominacion_db.nominado_set.all()
        if len(nominados_set) == len(nominados):
            #Ordeno la lista por nombre para comparacion lineal
            sorted(nominados_set, key=lambda nominado: nominado.nombre)
            iguales = True
            for i in range(numero_nominados):
                if nominados_set[i].nombre != nominados[i]:
                    iguales = False
                    break
            if iguales:
                #Si los conjuntos de nominados son iguales entonces hablamos de la misma nominacion
                nominacion = nominacion_db
            #Si no entonces seguimos buscando
    
    #Si no se encontro una nominacion en la base de datos igual entonces es una nueva nominacion
    if nominacion is None:
        nominacion = Nominacion(categoria=categoria)
        nominacion.save()
        for nombre_nominado in nominados:
            nom = Nominado(nombre = nombre_nominado, nominacion = nominacion)
            nom.save()

    #Se verifica voto unico:
    if VotoNominacion.objects.filter(user_id = user_id, nominacion = nominacion).exists():
        return redirect('/votaciones?msg=0')

    ###MEDIA###:
    media = Media()
    media.save()
    
    for nombre_file in request.FILES:
        file = request.FILES[nombre_file]
        if file.size <= 1.5*1024*1024 : # <= 1.5 MB
            foto      = media.foto_set.create(imagen=file, descripcion="")
            foto.imagen.delete(save=False)
            file.name = "__"+str(foto.pk)+"__"+file.name
            foto.imagen = file
            foto.save()
    
    for i in range(numero_videos):
        link_video = request.POST["video"+str(i)]
        media.video_set.create(link=link_video, descripcion="")
        
    ###Voto Final###:
    voto = VotoNominacion(user_id = user_id, nominacion = nominacion, media = media)
    voto.save()

    return redirect('/votaciones')



@login_required(login_url='login')
def consultar_nombre(request):
    respuesta = ""
    busqueda = request.GET['busqueda']

    busquedas = busqueda.split(' ')
    resultados = Carnet.objects.all()
    for b in busquedas:
        resultados = resultados.filter(nombre__icontains=b)

    if(resultados.exists()):
        respuesta  = resultados[0].nombre
    
    return HttpResponse(respuesta, mimetype='text/plain')



def votar(request):
    categorias = Categoria.objects.filter(edicion = Edicion.actual())

    #Nominaciones
    nominaciones = Nominacion.objects.filter(categoria__in = categorias)
    nominaciones = nominaciones.select_related('foto_id').select_related('nominado_set')


    medias = Media.objects.filter(votonominacion__in=nominaciones.values('votonominacion')).select_related('foto_id')

    votos = VotoFinal.objects.filter(user_id = request.user.pk).filter(nominacion__in = nominaciones)
    
    return render_to_response('votaciones/votar/index.html',
                              diccionario_base(
                                    {
                                    'categorias'   :categorias,
                                    'nominaciones' :nominaciones,
                                    'medias'       :medias,
                                    'votos'        :votos,
                                    }, request),
                              context_instance=RequestContext(request),
                              )


@login_required(login_url='login')
def votar_do(request):
    respuesta = None
    nominacion_id = int(request.POST['id'])

    try:
        voto = VotoFinal(user_id = request.user.pk, nominacion = Nominacion.objects.get(pk = nominacion_id))
        voto.save()
        respuesta = '1'
    except:
        respuesta = '0'

    return HttpResponse(respuesta, mimetype='text/plain')

@login_required(login_url='login')
def quitar_voto_do(request):
    respuesta = None
    categoria_id = int(request.POST['id'])
    
    try:
        voto = VotoFinal.objects.get(user_id = request.user.pk, nominacion__categoria = categoria_id)
        voto.delete()
        respuesta = '1'
    except:
        respuesta = '0'

    return HttpResponse(respuesta, mimetype='text/plain')



@login_required(login_url='login?next=login/')
def votaciones(request):
    EdicionActual = Edicion.objects.get(activa = True)

    if(EdicionActual.etapa == '0'): #cerrado
        return render_to_response('votaciones/cerrado/index.html',
                                  diccionario_base({}, request),
                                  context_instance=RequestContext(request),)
    if(EdicionActual.etapa == '1'): #nominando
        return nominaciones(request)
    if(EdicionActual.etapa == '2'): #filtrando
        return render_to_response('votaciones/filtrando/index.html',
                                  diccionario_base({}, request),
                                  context_instance=RequestContext(request),)
    if(EdicionActual.etapa == '3'): #votando
        return votar(request)
    else:
        raise Http404

    

def construccion(request):
    return render_to_response('votaciones/construccion/index.html',
                                diccionario_base({}, request),
                                context_instance=RequestContext(request),
                              )

@login_required(login_url='login')
def filtrar(request):
    if request.user.is_staff :
        categorias = Categoria.objects.filter(edicion = Edicion.actual())

        #Votos del Usuario
        votos        = VotoNominacion.objects.select_related('nominacion', 'nominacion__categoria','media').filter(user_id=request.user.pk)
        fotos        = Foto.objects.select_related('media').filter(media__in=votos.values('media'))
        videos       = Video.objects.select_related('media').filter(media__in=votos.values('media'))
        #Nominados a las nominaciones
        nominados    = Nominado.objects.filter(nominacion__in=votos.values('nominacion'))

        msg = None
        if(request.GET.__contains__('msg')):
            msg_id = request.GET['msg']
            if msg_id == "0":
                msg = "No puedes proponer dos veces la misma nominacion"

        return render_to_response('votaciones/filtrar/index.html',
                                  diccionario_base(
                                        {
                                        'votos'       :votos,
                                        'nominados'   :nominados,
                                        'categorias'  :categorias,
                                        'fotos'       :fotos,
                                        'videos'      :videos,
                                        'msg'         :msg,
                                        }, request),
                                  context_instance=RequestContext(request),
                                  )
    else:
        raise Http404

#
# vistas de Administrador:
#
@login_required(login_url='login')
def funcion(request):
    if request.user.is_staff :
        return render_to_response('votaciones/funcion/index.html',
                                diccionario_base({}, request),
                                context_instance=RequestContext(request),
                              )
    else:
        raise Http404

@login_required(login_url='login')
def funcion_do(request):
    if request.user.is_staff :
        carnets_raw = request.POST['carnets']

        lineas = carnets_raw.strip(' \t\n').splitlines()

        carnet = None
        for linea in lineas:
            partes = linea.split(' ',1)
            carnet_str = partes[0].strip()
            nombres    = partes[1].strip()

            if Carnet.objects.filter(numero=carnet_str).exists():
                continue

            carnet = Carnet(
                        numero = carnet_str.strip(),
                        nombre = nombres.strip(),
                        usado  = False
                        )
            carnet.save()

        return redirect(reverse('votaciones.views.funcion'))
    else:
        raise Http404



@login_required(login_url='login')
def limpiar_media(request):
    import os
    if request.user.is_staff :
        med = Media.objects.annotate(ref = Count('votonominacion')).filter(ref__lt=1)
        med.annotate(ref2 = Count('edicion')).filter(ref2__lt=1).delete()

        path = PROJECT_ROOT+"/media/media_subida/"
        imagenes = os.listdir(path)
        fotos = Foto.objects.values_list('imagen')

        for imagen in imagenes:
            if not ('media_subida/'+imagen,) in fotos:
                os.remove(path+imagen)

        return redirect('/admin')
    else:
        raise Http404