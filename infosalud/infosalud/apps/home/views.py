from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from infosalud.apps.notice.models import noticia, banner, recetas
from django.contrib.auth import authenticate, login,logout
#Llamado de Formularios
from infosalud.apps.security.forms import LoginForm
from infosalud.apps.home.forms import ContactForm
#LLamado de funcion para envio de emails
from django.core.mail import EmailMultiAlternatives #Enviar HTML
from django.core.paginator import Paginator, InvalidPage, EmptyPage
def index_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(username=username,password=password)
            if usuario is not None and usuario.is_active:
                login(request,usuario) #Creamos el login
    form = LoginForm() # Inicializamos un nuevo Formulario de login
    i=0
    noticia1 = []
    noticia2 = []
    noticias = noticia.objects.order_by('-id')[:4]
    i = 1
    for x in noticias:
        if i==1:
            noticia1 = x
            i += 1
        elif i <= 4: #Manejamos unicamente que nos envie solo 2 noticias en el index
            noticia2.append(x)
    importante = banner.objects.all().order_by('-id')[:6]
    ctx = {'noticia1':noticia1,'noticia2':noticia2,'banner':importante,'form':form}
    return render_to_response('home/index.html',ctx,context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def contacto_view(request):
	info_enviado = False
	email = ""
	titulo = ""
	texto = ""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email = formulario.cleaned_data['Email']
			titulo = formulario.cleaned_data['Titulo']
			texto = formulario.cleaned_data['Texto']
			#Configuracion enviando mensaje
			to_admin = 'infosaludvzla@gmail.com'
			html_content = "Informacion recibida por formulario.<br><br> **** MENSAJE *** <br>%s <br/> Titulo:%s <br/> Email: %s"%(texto,titulo,email)
			msg = EmailMultiAlternatives('Correo de contacto',html_content,'from@server.com',[to_admin])
			msg.attach_alternative (html_content,'text/html') #definimos el contenido como html
			msg.send()
	else:
		formulario = ContactForm()
	ctx = {'form_contacto':formulario,'email':email,'titulo':titulo,'texto':texto,'info_enviado':info_enviado,'form':LoginForm()}
	return render_to_response('home/contactanos.html',ctx,context_instance=RequestContext(request))

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return True
        else:
            return False
    else:
        return False
def donar(request):
    return render_to_response('noticia/donar.html',context_instance=RequestContext(request))