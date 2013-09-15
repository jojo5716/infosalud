# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponseRedirect
from infosalud.apps.security.forms import LoginForm,RegistrationStandardForm,RegistrationDoctorForm,edit_perfil_medico,edit_consultorio_medico,Registro_paciente,PostsMedicos,NoticiaMedicos,RecetaMedicos,ContactoMedico,ReportarMedico,responder_mensaje_medico,edit_newsletter
from infosalud.apps.security.models import userProfile,userDoctor,tipo_perfil, horariosMedico,Post,NoticiaMedico,RecetaMedico,noticias_medicos_ip,recetas_medicos_ip,mensajes_medicos
from infosalud.apps.notice.models import noticia,categorias_noticias,categorias_recetas,newsletter
from django.contrib.auth.models import User
from infosalud.apps.guias.models import especialidades
#Importamos lo siguiente para generar un activation Key
from django.core.signing import Signer
import datetime
from infosalud import settings
from django.utils.timezone import utc

def register_selection_view(request):
    return render_to_response('security/selectRegister.html',context_instance=RequestContext(request))


def register_view(request):
    emailUser = None
    if request.method == "POST":
        reg = RegistrationStandardForm(request.POST)
        if reg.is_valid():
            u_name = reg.cleaned_data['username']
            u_email = reg.cleaned_data['email']
            u_password = reg.cleaned_data['password']
            u_gender = reg.cleaned_data['gender']
            u_newsletter = reg.cleaned_data['newsletter']
            u = User.objects.create_user(u_name, u_email, u_password)
            u.is_active = False # Como default no activamos
            # Generamos una llave de activacion para enviarle a su correo.
            u.save() # Guardamos al usuario
            signer = Signer()
            salt = signer.sign(u.username)
            activation_key = salt
            now = datetime.datetime.utcnow().replace(tzinfo=utc) #Obtenemos la fecha actual según la zona horariaa
            key_expires = now + datetime.timedelta(2) # Creamos una fecha de expiracion por 3 dias
            p = userProfile()
            p.user = u # ligamos al usuario
            p.gender = u_gender
            p.activationKey = activation_key
            p.keyExpires = key_expires
            p.save() # Guardamos el perfil del Usuario.
            #Enviamos email de confirmacion.
            if u_newsletter:
                n = newsletter()
                n.usuario = u
                n.save()
            emailUser = u.email
            subject = 'Bienvenido a InfoSalud'
            from_email = 'from@server.com'
            to = emailUser
            text_content = ''
            html_content = '<p>Estamos muy contentos de que te encuentres con <strong> Nosotros !!!</strong></p><br>Tu Nombre de usuario es:    %s <br><br> Para activar tu cuenta por favor haz clic <a href="%s/cuenta/confirmar/%s/%s/">en este link</a> <br><br><h3> Esta cuenta debera ser confirmada en un lapso no mayor de 48 horas.</h3><h3>Atentamente: <strong>El equipo de InfoSalud.</strong></h3>'%(u.username,settings.URL_SERVER,u.username,p.activationKey)            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            mensaje = '<h2>Estimado: %s </h2><br/><h3>Hemos enviado un correo a: %s </h3>para que nos confirmes tu cuenta.<br><p> Esta cuenta deberá ser activada en las próximas 48 horas</p><br/><p> de lo contrario la solicitud será cancelada.</p><br/>InfoSalud Team.'
            ctx = {'mensaje':mensaje,'tipo':'exito'}
            return render_to_response('security/sendEmailConfirm.html',context_instance=RequestContext(request))
        else:
            form = LoginForm()
            ctx = {'form':form,'register_form':reg,'errores':'hubo errores en la validacion de los campos, revisa el correo eelectronico y usuario.'}
            return render_to_response('security/loginStandard.html',ctx,context_instance=RequestContext(request))
    else: # is get
        form = RegistrationStandardForm(initial={'newsletter':True})
    reg = RegistrationStandardForm()
    form = LoginForm()
    ctx = {'form':form,'register_form':reg,'email':emailUser}
    return render_to_response('security/loginStandard.html',ctx,context_instance=RequestContext(request))
def confirmAccount(request,user_name,activation_key):
    expired = False
    correctKey = False
    activatedUser = False
    new_user = User.objects.get(username__exact = user_name) # Encontramos al usuario
    mensaje = "en blanco" # iniciamos un mensaje
    if new_user.is_active: # Si el usuario ya esta activo entonces enviamos que si esta activado
        activatedUser = True
    else: # Si no esta activado entonces continuamos con el algoritmo
        if new_user is not None: # Si el usuario existe
            if new_user.get_profile().activationKey == activation_key: # Si la llave concuerda
                correctKey = True # La llave es correcta
                mensaje += "Llaves concuerdan, validamos la fecha"
                profile = new_user.get_profile()
                now = datetime.datetime.utcnow().replace(tzinfo=utc)
                if profile.keyExpires >= now: # Si no ha expirado el key entonces.
                    new_user.is_active = True # Activamos la cuenta del usuario
                    profile.activationKey = "ACTIVATED"
                    profile.keyExpires = None
                    profile.save() # Guardamos el perfil activado
                    new_user.save() # Activamos el usuario
                    activatedUser = True
                else:
                    expired = True
            else:
                correctKey = False
    ctx = {'user':new_user,'expired':expired,'correctKey':correctKey,'activatedUser':activatedUser,'URL_SERVER':settings.URL_SERVER}
    return render_to_response('security/confirmAccount.html',ctx,context_instance = RequestContext(request))
def register_doctor_view(request):
    if request.method == "POST":
        reg = RegistrationDoctorForm(request.POST)
        if reg.is_valid():
            print "entro"
            u_username = reg.cleaned_data['username']
            u_nombre = reg.cleaned_data['nombre']
            u_apellido = reg.cleaned_data['apellido']
            u_cedula = reg.cleaned_data['cedula']
            u_email = reg.cleaned_data['email']
            u_especialidad = reg.cleaned_data['especialidad']
            #u_fechanacimiento = reg.cleaned_data['fechaNac']
            u_licencia = reg.cleaned_data['numLicence']
            u_universidad = reg.cleaned_data['universidad']
            u_graduacion = reg.cleaned_data['graduacion']
            u_password = reg.cleaned_data['password']
            u_gender = reg.cleaned_data['gender']
            # Generamos una llave de activacion para enviarle a su correo.
            subject = 'Registro de nuevo medico'
            from_email = 'from@server.com'
            to = 'infosaludvzla@gmail.com'
            text_content = ''
            html_content = 'Nuevo medico registrado <br/><br/>Usuario:  %s <br/> Nombre: %s <br/> Apellido: %s <br/> Cedula: %s <br/> Email:%s <br/> Especialidad: %s <br/>  Sexo: %s <br/> Numero de licencia: %s <br/> Universidad: %s<br/> Ano de graduacion: %s <br/> Password: %s'%(u_username,u_nombre,u_apellido,u_cedula,u_email,u_especialidad,u_gender,u_licencia,u_universidad,u_graduacion,u_password)            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            mensaje = '<br/>InfoSalud Team.'
            ctx = {'mensaje':mensaje,'tipo':'exito'}
            return render_to_response('security/sendEmailConfirm.html',context_instance=RequestContext(request))
        else:
            print "no entro"
            form = LoginForm()
            ctx = {'form':form,'registerf':reg,'errores':'Hubo problemas al validad los datos introducidos, por favor revice que los datos son correctos.'}
    else: # is get
        reg = RegistrationDoctorForm()
        form = LoginForm()
    ctx = {'form':form,'registerf':reg}
    return render_to_response('security/loginMedico.html',ctx,context_instance=RequestContext(request))
def ver_perfil(request,id):
    id_visitar = int(id)
    if id_visitar == '':
        return HttpResponseRedirect('/')
    try:
        my_user = request.user
        my_id = int(my_user.id)
    except Exception, e:
        my_user = None
        my_id = None
    if str(id_visitar).isdigit():
        tipo = tipo_perfil(id_visitar)
        if tipo =="medico":
            tipo_medico = True
            yo = False
            usuario = User.objects.get(id__exact=id_visitar)
            especialidad = especialidades.objects.filter(userdoctor=id_visitar)

            try:
                horarios = horariosMedico.objects.filter(user_id__exact=id_visitar)
                for x in horarios:
                    hor_act = x.horario_act
                    prec_act = x.precios_act
                    direc_act=x.direccion_act
                    tlf_act = x.tlf_act
                    hor = x.horario
                    prec = x.precios
                    hor = hor.split(',')
                    prec = prec.split(',')    
                    direccion = x.direccion
                    tlf = x.tlf
                print prec
            except Exception, e:
                hor_act = False
                prec_act = False
                direc_act = False
                tlf_act = False
                hor = []
                prec = []
                direccion  = ''
                tlf = ''
            doc = userDoctor.objects.get(user_id__exact=id_visitar)
            post = Post.objects.filter(user_id__exact=id_visitar).count
            noticias = NoticiaMedico.objects.filter(user_id__exact=id_visitar).count
            receta = RecetaMedico.objects.filter(user_id__exact=id_visitar).count
            if id_visitar == my_id:
                yo=True
            else:
                yo = False
            ctx={'dato_user':usuario,'doctor':doc,'yo':yo,'post_count':post,'noticia_count':noticias,'receta_count':receta,'hor':hor,'prec':prec,'hor_act':hor_act,'direc_act':direc_act,'tlf_act':tlf_act,'prec_act':prec_act,'direccion':direccion,'tlf':tlf,'tipo_medico':tipo_medico,'especialidades':especialidad}
        else:
            yo = False
            if id_visitar == my_id:
                yo=True
                try:
                    news = newsletter.objects.get(usuario_id=my_id)
                    newslett = True
                except Exception, e:
                    newslett = False
                usuario = User.objects.get(id=my_id)
                try:
                    perfil_usuario = userProfile.objects.get(user_id=my_id)
                except Exception, e:
                    perfil_usuario = []
                
                if usuario.is_active:
                    if request.method == "GET":
                        noticias = noticia.objects.all().order_by('-id')[:4]
                        form = edit_newsletter(initial={
                            'newsletter':newslett
                            })
                        ctx = {"dato_user":usuario,'perfil':perfil_usuario,'yo':yo,'form':form,'subscrito':newslett,'id_usuario':my_id,'noticias':noticias}
                        return render_to_response('perfiles/usuario/perfil.html',ctx,context_instance=RequestContext(request))    
                    else:
                        form = edit_newsletter(request.POST)
                        if form.is_valid():
                            news = form.cleaned_data['newsletter']
                            if news:
                                n = newsletter()
                                n.usuario = usuario
                                n.save()
                                mensaje = "Te has suscrito con éxito a nuestro sistema de notificacion por email."
                                ctx = {"mensaje":mensaje,'tipo':"exito"}
                                return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
                            else:
                                n = newsletter.objects.get(usuario_id=my_id).delete()
                                mensaje = "Has eliminado la suscripcion con éxito."
                                ctx = {"mensaje":mensaje,'tipo':"exito"}
                                return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
                        else:
                            ctx = {"dato_user":usuario,'perfil':perfil_usuario,'yo':yo,'form':form,'subscrito':newslett,'id_usuario':my_id}
                            return render_to_response('perfiles/usuario/perfil.html',ctx,context_instance=RequestContext(request))
                else:
                    mensaje = "Aun no has activado tu perfil, revisa la bandeja de entrada del correo electronico que usaste al registrarte en InfoSalud."
                    ctx = {"mensaje":mensaje,'tipo':"error"}
                    return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))         
            else:
                mensaje = "Lo siento pero no puedes ver este perfil."
                ctx = {"mensaje":mensaje,'tipo':"error"}
                return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))   
        return render_to_response('perfiles/'+tipo+'/perfil.html',ctx,context_instance=RequestContext(request))

def verificar_pass():
    if request.method=="POST":
        form = editar_perfil_2(request.POST)
        if form.is_valid():
            print "Es valido las claves."
def verificar_email(email_u):
    if not User.objects.filter(email=email_u).exists():
        return False
    else:
        return True
def agregar_user(request,id):
    try:
        my_user = request.user
        my_id = int(my_user.id)
        id_user_get= int(id)
    except Exception, e:
        print "No esta logueado"
    if my_id == id_user_get:
        tipo = tipo_perfil(my_id)
    if tipo =="medico":
        if request.method == "GET":
            return render_to_response('perfiles/medico/agregar_user.html',context_instance=RequestContext(request))
        else:
            mensaje = "No eres medico, no puedes ver esta seccion."
            return mensaje
    else:
        mensaje = "No pudes ver esta seccion."
        return mensaje
def crear_user(request):
    if request.method == "POST":
        print "si esta entrando al post "
        reg = Registro_paciente(request.POST)
        print reg
        if reg.is_valid():
            print "entro"
            u_name = reg.cleaned_data['username']
            u_first_name = reg.cleaned_data['nombre']
            u_last_name = reg.cleaned_data['apellido']
            u_dni = reg.cleaned_data['dni']
            u_email = reg.cleaned_data['email']
            u_password = reg.cleaned_data['password']
            u_gender = reg.cleaned_data['gender']
            u_estado = reg.cleaned_data['estado']
            u_ciudad = reg.cleaned_data['ciudad']
            u_edo_civil = reg.cleaned_data['edoCivil']
            u_tlf_cel = reg.cleaned_data['tlf_cel']
            u_tlf_casa = reg.cleaned_data['tlf_casa']
            u = User.objects.create_user(u_name, u_email, u_password)
            u.is_active = False # Como default no activamos
            # Generamos una llave de activacion para enviarle a su correo.
            u.save() # Guardamos al usuario
            signer = Signer()
            salt = signer.sign(u.username)
            activation_key = salt
            key_expires = datetime.datetime.today() + datetime.timedelta(2) # Creamos una fecha de expiracion por 3 dias
            p = userProfile()
            p.user = u # ligamos al usuario
            p.activationKey = activation_key
            p.keyExpires = key_expires
            p.gender = u_gender
            p.fechaNacimiento = reg.cleaned_data['fechaNacimiento']
            p.save() # Guardamos el perfil del Usuario.
            #Enviamos email de confirmacion.
            emailUser = u.email
            subject = 'Bienvenido a InfoSalud'
            from_email = 'from@server.com'
            to = emailUser
            text_content = ''
            html_content = '<p>We are happy to get you <strong> Here !!!</strong>:)</p><br>Your username is:    %s <br><br> To activate your Acount Please <a href="http://%s/accounts/confirm/%s/%s/">click HERE</a> to confirm your email <br><br><h3>Sincerily: <strong>Eyventu Team</strong></h3>'%(u.username,settings.URL_SERVER,u.username,p.activationKey)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render_to_response('security/sendEmailConfirm.html',context_instance=RequestContext(request))
        else:
            pass
                
    else: # is get
        form = Registro_paciente()
    reg = Registro_paciente()
    form = LoginForm()
    ctx = {'form':form,'register_form':reg,'mensaje':mens}
    return render_to_response('perfiles/medico/crear_paciente.html',ctx,context_instance=RequestContext(request))

def post_medico(request,id):
    if request.is_ajax():
        id_user_get= int(id)
        try:
            my_user = request.user
            my_id = int(my_user.id)
        except Exception, e:
            my_user=None
            my_id=None
        yo = False
        try:
            post_medico = Post.objects.filter(user_id__exact=id_user_get).order_by('-id')
            print str(id_user_get)
            print str(post_medico)
        except Exception, e:
            post_medico = "No hay post para mostrar."
        doc = userDoctor.objects.get(user_id=id_user_get)
        if id_user_get == my_id:
            yo = True
            if request.method == "POST":
                f_post = PostsMedicos(request.POST)
                if f_post.is_valid():
                    post = f_post.cleaned_data['post']
                    p = Post()
                    p.user_id = my_id
                    p.post = post
                    p.save()
                    mensaje = "Tu post fue creado con exito."
                    ctx = {"mensaje":mensaje,'tipo':"exito"}
                    return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
            else:
                f_post = PostsMedicos()
                ctx = {'form':f_post,'form_act':True,'yo':True,'post_m':post_medico,'doc':doc}
                return render_to_response('perfiles/medico/post.html',ctx,context_instance=RequestContext(request))
        else:
            ctx = {'post_m':post_medico,'yo':False,'form_act':False,'doc':doc}
            return render_to_response('perfiles/medico/post.html',ctx,context_instance=RequestContext(request))
    else:
        mensaje = "No estas autorizado para realizar esta operacion."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
def noticia_medico(request,id):
    if request.is_ajax():
        id_user_get= int(id)
        try:
            my_user = request.user
            my_id = int(my_user.id)
        except Exception, e:
            my_user=None
            my_id=None 
        yo = False
        try:
            noticia_medico = NoticiaMedico.objects.filter(user_id__exact=id_user_get).order_by('-id')
        except Exception, e:
            noticia_medico = "No hay noticias de este medico."  
        doc = userDoctor.objects.get(user_id=id_user_get)
        if my_id == id_user_get:
            yo = True
            if request.method == "POST":
                print request.POST
                f_noticia = NoticiaMedicos(request.POST)
                if f_noticia.is_valid():
                    print "formulario valido"
                    noticia = f_noticia.cleaned_data['noticia'] 
                    titulo = f_noticia.cleaned_data['titulo']
                    categoria = request.POST['categoria']
                    if str(categoria) == '000':
                        ca = request.POST['nuevaCategoria']
                        print ca
                        cat = categorias_noticias()
                        cat.categoria=str(ca)
                        cat.save()
                        ca = categorias_noticias.objects.get(categoria=ca)
                        categoria = ca.id
                    print str(categoria)
                    n = NoticiaMedico()
                    n.user_id=my_id
                    n.titulo = titulo
                    n.noticia = noticia
                    n.categoria_id=categoria
                    n.tiempo_registro="2013-02-07 21:02:02 -0430"
                    n.save()
                    mensaje = "Tu noticia fue creada con exito."
                    ctx = {"mensaje":mensaje,'tipo':"exito"}
                    return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
            else:
                f_noticia = NoticiaMedicos()
                categoria_noticia= categorias_noticias.objects.all()
                ctx = {'form':f_noticia,'form_act':True,'yo':True,'noticia_m':noticia_medico,'cat':categoria_noticia,'doc':doc}
                return render_to_response('perfiles/medico/noticias.html',ctx,context_instance=RequestContext(request))
        else:
            ctx = {'form_act':False,'yo':False,'noticia_m':noticia_medico,'doc':doc}
            return render_to_response('perfiles/medico/noticias.html',ctx,context_instance=RequestContext(request))
    else:
        mensaje = "No estas autorizado para realizar esta operacion."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))

def receta_medico(request,id):
    if request.is_ajax():
        id_user_get= int(id)
        try:
            my_user = request.user
            my_id = int(my_user.id)
        except Exception, e:
            my_user=None
            my_id=None 
        yo = False
        try:
            receta_medico = RecetaMedico.objects.filter(user_id__exact=id_user_get).order_by('-id')
        except Exception, e:
            receta_medico = "No hay recetas de este medico."  
        doc = userDoctor.objects.get(user_id=id_user_get)
        if my_id == id_user_get:
            yo = True
            if request.method == "POST":
                print request.POST
                f_receta = RecetaMedicos(request.POST, request.FILES)
                if f_receta.is_valid():
                    titulo = f_receta.cleaned_data['titulo']
                    categoria = request.POST['categoria']
                    preparacion = f_receta.cleaned_data['preparacion']
                    ingredientes = f_receta.cleaned_data['ingredientes']
                    tiempo = f_receta.cleaned_data['tiempo']
                    if str(categoria) == '000':
                        ca = request.POST['nuevaCategoria']
                        print ca
                        cat = categorias_recetas()
                        cat.categoria=str(ca)
                        cat.save()
                        ca = categorias_recetas.objects.get(categoria=ca)
                        categoria = ca.id
                    print str(categoria)
                    n = RecetaMedico()
                    n.user_id=my_id
                    n.titulo = titulo
                    n.ingredientes = ingredientes
                    n.preparacion = preparacion
                    n.tiempo = tiempo
                    n.categoria_id=categoria
                    n.tiempo_registro="2013-02-07 21:02:02 -0430"
                    n.save()
                    mensaje = "Tu receta fue creada con exito."
                    ctx = {"mensaje":mensaje,'tipo':"exito"}
                    return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
                else:
                    pass
            else:
                f_receta = RecetaMedicos()
                categoria_receta= categorias_recetas.objects.all()
                ctx = {'form':f_receta,'form_act':True,'yo':True,'receta_m':receta_medico,'cat':categoria_receta,'doc':doc}
                return render_to_response('perfiles/medico/receta.html',ctx,context_instance=RequestContext(request))
        else:
            ctx = {'form_act':False,'yo':False,'receta_m':receta_medico,'doc':doc}
            return render_to_response('perfiles/medico/receta.html',ctx,context_instance=RequestContext(request))
    else:
        mensaje = "No estas autorizado para realizar esta operacion."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
def ver_noticia_medico(request,id):
    try:
        visitar = int(id)
        noticia = NoticiaMedico.objects.get(id__exact=visitar)
        autor_id = noticia.user_id
        autor = User.objects.get(id__exact = int(autor_id))
        url = "www.infosalud.co.ve/ver_noticia_medico/"+str(visitar)
        ctx = {'noticia':noticia,'autor':autor,'url':url}
        return render_to_response('perfiles/medico/ver_noticia.html',ctx,context_instance=RequestContext(request))
    except Exception, e:
        mensaje = "Lo lamento pero esta noticia no existe."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
def ver_receta_medico(request,id):
    try:
        visitar = int(id)
        receta = RecetaMedico.objects.filter(id__exact=visitar)
        for x in receta:
            ingredientes = x.ingredientes
            preparacion = x.preparacion
            titulo = x.titulo
            tiempo = x.tiempo
            imagen = x.imagen
            receta_id = x.id
            autor_id = int(x.user_id)
        print "Autor ID: "+str(autor_id)
        ingre = ingredientes.split(',')
        prepa = preparacion.split(',')
        autor = User.objects.get(id__exact = autor_id)
        ctx = {'autor':autor,'autor_id':autor_id,'ingredientes':ingre,'preparacion':prepa,'titulo':titulo,'tiempo':tiempo,'imagen':imagen,'receta_id':receta_id}
        return render_to_response('perfiles/medico/ver_receta.html',ctx,context_instance=RequestContext(request))
    except Exception, e:
        mensaje = "Lo lamento pero esta receta no existe."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
def rate_recetas_medicos(request):
    if request.is_ajax():
        if request.method == "GET":
            print "aqui estamos"
            id_n = int(request.GET['id'])
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            buscar = recetas_medicos_ip.objects.filter(receta_ip=ip,receta_id=id_n)
            cant = buscar.count()
            if cant == 0:
                recetaV = RecetaMedico.objects.get(id__exact=id_n)
                n_vot= recetaV.n_votos
                recetaV.n_votos = n_vot + 1
                recetaV.save()
                nv = recetas_medicos_ip()
                nv.receta_id= id_n
                nv.receta_ip = ip
                nv.save()
                mensaje= "Total de votos:"+str(n_vot + 1)
                ctx={'msg':mensaje}
            else:
                mensaje= "Ya votaste esta receta."
                ctx={'msg':mensaje}
        else:
            mensaje= 'Disculpe su voto no pudo ser procesado.'
            ctx={'msg':mensaje}
    else:
        mensaje = 'No puede entrar a esta seccion'
        ctx = {'msg':mensaje }     
    return render_to_response('noticia/votos.html',ctx,context_instance=RequestContext(request))
def rate_noticias_medicos(request):
    if request.is_ajax():
        if request.method == "GET":
            print "aqui estamos"
            id_n = int(request.GET['id'])
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            buscar = noticias_medicos_ip.objects.filter(noticia_ip=ip,noticia_id=id_n)
            cant = buscar.count()
            if cant == 0:
                noticiaV = NoticiaMedico.objects.get(id__exact=id_n)
                n_vot= noticiaV.n_votos
                noticiaV.n_votos = n_vot + 1
                noticiaV.save()
                nv = noticias_medicos_ip()
                nv.noticia_id= id_n
                nv.noticia_ip = ip
                nv.save()
                mensaje= "Total de votos:"+str(n_vot + 1)
                ctx={'msg':mensaje}
            else:
                mensaje= "Ya votaste esta noticia."
                ctx={'msg':mensaje}
        else:
            mensaje= 'Disculpe su voto no pudo ser procesado.'
            ctx={'msg':mensaje}
    else:
        mensaje = 'No puede entrar a esta seccion'
        ctx = {'msg':mensaje }     
    return render_to_response('noticia/votos.html',ctx,context_instance=RequestContext(request))
def contacto_medicos(request,id):
    if request.is_ajax():
        id_medico= int(id)
        try:
            my_user = request.user
            my_id = int(my_user.id)
            print "ID: --->>> "+str(id_medico)
            print "-_-_-_-_-_-_-_-_"
        except Exception, e:
            mensaje = "Lo lamento pero debes estar logueado para entrar en esta seccion."
            ctx = {"mensaje":mensaje,'tipo':"error"}
            return render_to_response('mensajes/mensajes_ajax.html',ctx,context_instance=RequestContext(request))
        print "ID: "+str(id_medico)
        if request.method == "POST":
            doctor = User.objects.get(id__exact=id_medico)
            f_contacto = ContactoMedico(request.POST)
            if f_contacto.is_valid():
     
                titulo = f_contacto.cleaned_data['titulo']
                mensaje = f_contacto.cleaned_data['mensaje']
                mensa = mensajes_medicos()
                mensa.titulo = titulo
                mensa.mensaje = mensaje
                mensa.autor = my_user
                mensa.medico = doctor
                mensa.save()

                mensaje = "Felicidades, el mensaje se ha enviado con exito."
                ctx = {"mensaje":mensaje,'tipo':"exito"}
                return render_to_response('mensajes/mensajes_ajax.html',ctx,context_instance=RequestContext(request))
        else:
            f_contacto = ContactoMedico()
            ctx = {'form':f_contacto,'id_medico':id_medico}
            return render_to_response('perfiles/medico/contacto.html',ctx,context_instance=RequestContext(request))
    else:
        mensaje = "Para ingresar al formulario de contacto para medicos, debera entrar en su perfil y estar logueado."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
def reportar_medico(request,id):
    if request.is_ajax():
        id_medico = int(id)
        try:
            my_user = request.user
            my_id = int(my_user.id)
        except Exception, e:
            mensaje = "Lo lamento pero debes estar logueado para entrar en esta seccion."
            ctx = {"mensaje":mensaje,'tipo':"error"}
            return render_to_response('mensajes/mensajes_ajax.html',ctx,context_instance=RequestContext(request))
        if request.method=="POST":
            doctor = User.objects.get(id__exact=id_medico)
            f_reportar = ReportarMedico(request.POST)
            if f_reportar.is_valid():
                email_user = my_user.email
                nombre_user = my_user.first_name
                apellido_user = my_user.last_name
                mensaje = f_reportar.cleaned_data['mensaje']
                subject = "Reportando medico"
                from_email = 'from@server.com'
                to = 'InfoSaludvzla@gmail.com'
                text_content=''
                html_content = 'prueba'
                html_content2 = '<span>Le informamos que el Usuario:</span><br/> <span>Nombre: %s <br/> Apellido: %s <br/> Email: <br/> </span> <br/> <span>A sido denunciado por el Usuario</span><br/><span> Nombre: %s <br/> Apellido: %s <br/> Email: %s <br/> </span><span>Motivo de la denuncia: <br/></span><span>%s</span>'%(doctor.first_name,doctor.last_name,doctor.email,nombre_user,apellido_user,email_user,mensaje)
                msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
                msg.attach_alternative(html_content,"text/html")
                msg.send()
                mensaje = "Gracias por contar con nosotros, analizaremos el email que nos has enviado y pronto estaremos en contacto contigo. Recuerda que en InfoSalud estamos para servirte."
                ctx = {"mensaje":mensaje,'tipo':"exito"}
                return render_to_response('mensajes/mensajes_ajax.html',ctx,context_instance=RequestContext(request))
            else:
                mensaje = 'Hubo un error al validar el formulario, revisa que el campo este correcto, que no contenga simbolos como <span style="color:red;"></span>'
                ctx = {"mensaje":mensaje,'tipo':"exito"}
                return render_to_response('mensajes/mensajes_ajax.html',ctx,context_instance=RequestContext(request))
        else:
            f_reportar = ReportarMedico()
            ctx = {'form':f_reportar,'id_medico':id_medico}
            return render_to_response('perfiles/medico/reportar.html',ctx,context_instance=RequestContext(request))
    else:
        mensaje = "Para poder reportar un medico, debera entrar en su perfil y estar logueado."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
def ver_mis_mensajes_medico(request,id):
    if User.is_authenticated:
        id_medico = int(id)
        my_user = request.user
        my_id = int(my_user.id)
        tipo = tipo_perfil(id)
        if tipo =="medico":
            yo = False
            if id_medico == my_id:
                yo = True
                mensajes = mensajes_medicos.objects.filter(medico_id=id_medico).order_by('-id')
                ctx = {'mensajes':mensajes,'yo':yo,'medico':id_medico}
                return render_to_response('perfiles/medico/mis_mensajes.html',ctx,context_instance=RequestContext(request))
    else:
        mensaje = "Para poder reportar un medico, debera entrar en su perfil y estar logueado."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
def leer_mensaje(request,id,id_medic):
    if User.is_authenticated:
            id_medico = int(id_medic)
            my_user = request.user
            my_id = int(my_user.id)
            tipo = tipo_perfil(my_id)
            if tipo =="medico":
                yo = False
                if id_medico == my_id:
                    mensaje = mensajes_medicos.objects.get(pk=id,medico_id=id_medico)
                    autor_mensaje = int(mensaje.autor_id)
                    if request.method == "GET":
                        form = responder_mensaje_medico()
                        yo=True
                        autor = User.objects.get(pk=autor_mensaje)
                        try:
                            perfil_autor = userProfile.objects.get(user_id=autor_mensaje)
                        except Exception, e:
                            perfil_autor = userDoctor.objects.get(user_id=autor_mensaje)
                        ctx = {'mensaje':mensaje,'yo':yo,'autor':autor,'perfil_autor':perfil_autor,'form':form,'id_mensaje':id,'id_medico':id_medico}
                        return render_to_response('perfiles/medico/leer_mensaje.html',ctx,context_instance=RequestContext(request))
                    else:
                        form = responder_mensaje_medico(request.POST)
                        if form.is_valid():
                            mensaje = form.cleaned_data['mensaje']
                            autor = User.objects.get(pk=autor_mensaje)
                            doctor = User.objects.get(pk=my_id)
                            subject = 'Respuesta de medico %s %s'%(doctor.first_name,doctor.last_name)
                            from_email = 'from@server.com'
                            to = autor.email
                            text_content = ''
                            html_content = 'Hola %s %s el medico %s %s ha respondido su mensaje:<br/> %s'%(autor.first_name,autor.last_name,doctor.first_name,doctor.last_name,mensaje)
                            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                            mensaje = "Su respuesta ha sido exitosa"
                            ctx = {"mensaje":mensaje,'tipo':"exito"}
                            return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
    mensaje = "Acceso denegado"
    ctx = {"mensaje":mensaje,'tipo':"error"}
    return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
        
def responder_mensaje(request):
    pass
def editar_perfil_medico(request,id):
    id_medico = int(id)
    try:
        my_user = request.user
        my_id = int(my_user.id)
    except Exception, e:
        mensaje = "Acceso denegado."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
    tipo = tipo_perfil(id_medico)
    if tipo =="medico":
        yo = False
        if id_medico == my_id:
            if request.method == "GET":
                datos_medico = User.objects.get(id__exact=id_medico)
                datos_perfil = userDoctor.objects.get(user_id__exact=id_medico)
                form_editar = edit_perfil_medico(initial={
                                                   'email':datos_medico.email,
                    })
                ctx = {'form':form_editar,'dato_user':datos_medico,'doctor':datos_perfil}
                return render_to_response('perfiles/medico/editar_info.html',ctx,context_instance=RequestContext(request))
            else:

                doctor = User.objects.get(id__exact=id_medico)
                perfil_doctor = userDoctor.objects.get(user_id__exact=id_medico)
                
                form = edit_perfil_medico(request.POST,request.FILES)
                if form.is_valid():
                    u_email = form.cleaned_data['email']
                    u_imagen = form.cleaned_data['photo']
                    if u_imagen:
                        perfil_doctor.photo=u_imagen
                    doctor.email = u_email
                    doctor.save()
                    perfil_doctor.save()
                    print "exito"
                else:
                    print "no funciona"
                    ctx = {'form':form,'dato_user':doctor,'doctor':perfil_doctor}
                    return render_to_response('perfiles/medico/editar_info.html',ctx,context_instance=RequestContext(request))

def editar_consultorio_medico(request,id):
    id_medico = int(id)
    try:
        my_user = request.user
        my_id = int(my_user.id)
    except Exception, e:
        mensaje = "Acceso denegado."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
    tipo = tipo_perfil(id_medico)
    if tipo =="medico":
        yo = False
        if id_medico == my_id:
            if request.method == "GET":
                datos_medico = User.objects.get(id__exact=id_medico)
                datos_perfil = userDoctor.objects.get(user_id__exact=id_medico)
                try:
                    datos_consultorio = horariosMedico.objects.filter(user_id__exact=id_medico)
                    for x in datos_consultorio:
                        hor_act = x.horario_act
                        prec_act = x.precios_act
                        direc_act=x.direccion_act
                        tlf_act = x.tlf_act
                        hor2 = x.horario
                        prec2 = x.precios
                        hor = x.horario
                        prec = x.precios
                        hor = hor.split(',')
                        prec = prec.split(',')    
                        direccion = x.direccion
                        horario = x.horario.split('-')
                        tlf = x.tlf
                except Exception, e:
                    hor_act = False
                    prec_act = False
                    direc_act = False
                    tlf_act = False
                    hor = []
                    prec = []
                    direccion  = ''
                    tlf = ''
                try:
                    form_editar = edit_consultorio_medico(initial={
                              'direccion':direccion,
                              'telefono':tlf,
                              'horarios':hor2,
                              'precios':prec2,
                              'direccion_act':direc_act,
                              'horarios_act':hor_act,
                              'telefono_act':tlf_act,
                              'precios_act':prec_act,
                        })

                    ctx={'form':form_editar,'dato_user':datos_medico,'doctor':datos_perfil,'hor':hor,'prec':prec,'hor_act':hor_act,'direc_act':direc_act,'tlf_act':tlf_act,'prec_act':prec_act,'direccion':direccion,'tlf':tlf,'id_medico':my_id}
                except Exception, e:
                    form_editar = edit_consultorio_medico()
                    ctx = {'form':form_editar,'dato_user':datos_medico,'doctor':datos_perfil,'id_medico':my_id}
                return render_to_response('perfiles/medico/datos_consultorio.html',ctx,context_instance=RequestContext(request))
            else:
                form_editar = edit_consultorio_medico(request.POST)
                if form_editar.is_valid():
                    my_user = request.user
                    my_id = int(my_user.id)
                    direc = form_editar.cleaned_data['direccion']
                    horarios = form_editar.cleaned_data['horarios']
                    precios = form_editar.cleaned_data['precios']
                    telefono = form_editar.cleaned_data['telefono']
                    direc_act = form_editar.cleaned_data['direccion_act']
                    hora_act = form_editar.cleaned_data['horarios_act']
                    telefono_act = form_editar.cleaned_data['telefono_act']
                    prec_act = form_editar.cleaned_data['precios_act']
                    try:
                        hora = horariosMedico.objects.get(user_id=my_id)
                    except Exception, e:
                        hora = horariosMedico()
                    hora.user_id = my_id
                    hora.direccion = direc 
                    hora.horario = horarios
                    hora.precios = precios
                    hora.tlf = telefono
                    hora.horario_act = hora_act
                    hora.direccion_act = direc_act
                    hora.precios_act = prec_act
                    hora.tlf_act = telefono_act
                    hora.save()
                    print "todo guardado"
                    mensaje = "Felicidades. Has actualizado tu nuevo horario."
                    ctx = {"mensaje":mensaje,'tipo':"exito"}
                    return render_to_response('mensajes/mensajes_ajax.html',ctx,context_instance=RequestContext(request))
                else:
                    ctx = {"form":form_editar}
                    return render_to_response('perfiles/medico/datos_consultorio.html',ctx,context_instance=RequestContext(request))
                    