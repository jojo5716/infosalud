from django.shortcuts import render_to_response
from django.template import RequestContext
from infosalud.apps.notice.models import noticia, recetas,noticias_ip,categorias_noticias,categorias_recetas,recetas_ip

from infosalud.apps.security.forms import LoginForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import operator
def notice_view(request,id_n):
	notice = noticia.objects.get(id=id_n)
	ctx = {'noticia':notice,'form':LoginForm()}
	return render_to_response('noticia/noticia.html',ctx,context_instance=RequestContext(request))

def recomendar_view(request):
    if request.is_ajax():
        if request.method == "GET":
            cat = str(request.GET['recomendar'])
            recomend = noticia.objects.filter(categoria=cat)
            ctx = {'recomendar':recomend}
    return render_to_response('noticia/recomendadas.html',ctx,context_instance=RequestContext(request))
def recomendar_receta_view(request):
    if request.is_ajax():
        if request.method == "GET":
            cat = str(request.GET['recomendar'])
            recomend = recetas.objects.filter(categoria__exact=cat)
            ctx = {'recomendar':recomend}
    return render_to_response('recetas/recomendadas.html',ctx,context_instance=RequestContext(request))

def rate_view(request):
    if request.is_ajax():
        if request.method == "GET":
            id_n = int(request.GET['id'])
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            buscar = noticias_ip.objects.filter(noticia_ip=ip,noticia_id=id_n)
            cant = buscar.count()
            if cant == 0:
                noticiaV = noticia.objects.get(id__exact=id_n)
                n_vot= noticiaV.n_votos
                noticiaV.n_votos = n_vot + 1
                noticiaV.save()
                nv = noticias_ip()
                nv.noticia_id= id_n
                nv.noticia_ip = ip
                nv.save()
                mensaje= 'Total de votos: '+str(n_vot + 1)
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
def rate_view_recetas(request):
    if request.is_ajax():
        if request.method == "GET":
            id_n = int(request.GET['id'])
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            buscar = recetas_ip.objects.filter(recetas_ip=ip,recetas_id=id_n)
            cant = buscar.count()
            if cant == 0:
                recetaV = recetas.objects.get(id__exact=id_n)
                n_vot= recetaV.n_votos
                recetaV.n_votos = n_vot + 1
                recetaV.save()
                nv = recetas_ip()
                nv.receta_id= id_n
                nv.receta_ip = ip
                nv.save()
                mensaje= 'Total de votos: '+str(n_vot + 1)
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
def all_noticias(request,pagina):
    noticias = None
    lista_noticias = noticia.objects.all().order_by('-id')
    categoria_noticias= categorias_noticias.objects.all()
    paginator = Paginator(lista_noticias, 3)
    try:
        page = int(pagina)
    except ValueError:
        page = 1
    try:
        noticias = paginator.page(page)
    except (EmptyPage, InvalidPage):
        noticias = paginator.page(paginator.num_pages)
    ctx = {"noticia": noticias ,'form':LoginForm(),'cate':categoria_noticias}
    return render_to_response('noticia/noticias_all.html',ctx,context_instance=RequestContext(request))

def all_recetas(request,pagina):
    rece = None
    lista_recetas = recetas.objects.all().order_by('-id')
    for x in lista_recetas:
        ingredientes = x.ingredientes
    ingre = ingredientes.split(',')
    categoria_recetas= categorias_recetas.objects.all()
    paginator = Paginator(lista_recetas, 3)
    try:
        page = int(pagina)
    except ValueError:
        page = 1
    try:
        rece = paginator.page(page)
    except (EmptyPage, InvalidPage):
        rece = paginator.page(paginator.num_pages)
        #ctx = {"noticias": noticias }
    ctx = {'receta':rece,'form':LoginForm(),'cate':categoria_recetas,'ingredientes':ingre}
    return render_to_response('recetas/recetas_all.html',ctx,context_instance=RequestContext(request))
def recetas_view(request,id_r):
    receta = recetas.objects.get(id__exact=id_r)
    ingredientes = receta.ingredientes
    preparacion = receta.preparacion
    prepa = preparacion.split(',')
    ingre = ingredientes.split(',')
    ctx = {'receta':receta,'form':LoginForm(),'ingredientes':ingre,'preparacion':prepa}
    return render_to_response('recetas/receta.html',ctx,context_instance=RequestContext(request))

def ordenar_noticia(request,secc,orde,pagina):
    if request.method=="GET":
        categoria_noticias= categorias_noticias.objects.all()
        noticias = None
        seccion = str(secc)
        orden = str(orde)
        print seccion
        print orden

        try:        
            if seccion=="categoria":
                orden = int(orden)
                noticias = noticia.objects.filter(categoria_id=orden).order_by('-id')
            elif seccion=="votos":
                if orden=="mas":
                    noticias = noticia.objects.all().order_by('-n_votos')
                    print noticias
                elif orden =="menos":
                    noticias = noticia.objects.all().order_by('n_votos')
            elif seccion == "id":
                if orden == "id":
                    noticias = noticia.objects.all().order_by('-id')
                elif orden =="mid":
                    noticias = noticia.objects.all().order_by('id')
            paginator = Paginator(noticias, 3)
            try:
                page = int(pagina)
            except ValueError:
                page = 1
            try:
                noti = paginator.page(page)
            except (EmptyPage, InvalidPage):
                noti = paginator.page(paginator.num_pages)

            ctx = {'noticia':noti,'seccion':secc,'orden':orden,'cate':categoria_noticias}
            return render_to_response('noticia/noticias_ordenadas.html',ctx,context_instance=RequestContext(request))


        except Exception, e:
                mensaje = "Lo siento pero hubo un problema."
                ctx = {"mensaje":mensaje,'tipo':"error"}
                return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))  

    else:
        mensaje = "Lo siento pero hubo un problema."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))  

def ordenar_receta(request,secc,orde,pagina):
    if request.method=="GET":
        categoria_recetas= categorias_recetas.objects.all()
        rec = None
        seccion = str(secc)
        orden = str(orde)
        try:
            if seccion == "categoria":
                orden = int(orden)
                rece=recetas.objects.filter(categoria_id=orden).order_by('-id')
                print rece
            elif seccion =="votos":
                if orden =="mas":
                    rece = recetas.objects.all().order_by('-n_votos')
                    print rece
                    print "-..-.-.-.-."
                else:
                    rece = recetas.objects.all().order_by('n_votos')
            elif seccion =="id":
                if orden =="id":
                    rece = recetas.objects.all().order_by('-id')
                else:
                    rece = recetas.objects.all().order_by('id')
            paginator = Paginator(rece,3)
            try:
                page = int(pagina)
            except ValueError:
                page = 1
            try:
                re = paginator.page(page)
            except (EmptyPage, InvalidPage):
                re = paginator.page(paginator.num_pages)
            ctx = {'receta':re,'seccion':seccion,'orden':orden,'cate':categoria_recetas}
            return render_to_response('recetas/recetas_ordenadas.html',ctx,context_instance=RequestContext(request))

        except Exception, e:
            raise e