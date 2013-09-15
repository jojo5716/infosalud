from django.shortcuts import render_to_response
from django.template import RequestContext
from infosalud.apps.enfermedades.models import glosario,enfermedad,sintoma 
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from infosalud.apps.security.models import userDoctor

def glosario_view(request,pagina):
    glo = None
    lista_glosario = glosario.objects.all().order_by('nombre')
    paginator = Paginator(lista_glosario, 1)
    try:
        page = int(pagina)
    except ValueError:
        page = 1
    try:
        glo = paginator.page(page)
    except (EmptyPage, InvalidPage):
        glo = paginator.page(paginator.num_pages)
    alfab = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    ctx = {"glosario": glo,"abc":alfab,'seccion':"glosario"}
    return render_to_response('glosario/glosario.html',ctx,context_instance=RequestContext(request)) 

def glosario_view_ordenado_alfabeto(request,letra):
    l = str(letra)
    glo= glosario.objects.filter(nombre__startswith=l).values('nombre')
    alfab = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    ctx={'glosario':glo,"abc":alfab,'seccion':"glosario"}
    return render_to_response('glosario/glosario.html',ctx,context_instance=RequestContext(request))
def ver_glosario(request,id):
	id_glosario= int(id)
	glo = glosario.objects.get(id__exact=id_glosario)
	ctx = {'glosario':glo}
	return render_to_response('glosario/ver_glosario.html',ctx,context_instance=RequestContext(request))
def enfermedades_view(request,pagina):
    enfe = None
    lista_enfe = enfermedad.objects.all().order_by('nombre')
    paginator = Paginator(lista_enfe, 1)
    try:
        page = int(pagina)
    except ValueError:
        page = 1
    try:
        enfe = paginator.page(page)
    except (EmptyPage, InvalidPage):
        enfe = paginator.page(paginator.num_pages)
    alfab = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    ctx = {"enfermedad": enfe,"abc":alfab,'seccion':"enfermedad"}
    return render_to_response('glosario/enfermedades.html',ctx,context_instance=RequestContext(request)) 
def sintomas_view(request,pagina):
    sinto = None
    lista_sinto = sintoma.objects.all().order_by('nombre')
    print lista_sinto
    paginator = Paginator(lista_sinto, 1)
    try:
        page = int(pagina)
    except ValueError:
        page = 1
    try:
        sinto = paginator.page(page)
    except (EmptyPage, InvalidPage):
        sinto = paginator.page(paginator.num_pages)
    alfab = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    ctx = {"sintoma": sinto,"abc":alfab,'seccion':"sintomas"}
    return render_to_response('glosario/sintomas.html',ctx,context_instance=RequestContext(request)) 
def sintomas_view_ordenado_alfabeto(request,letra,pagina):
    l = str(letra)
    lista_sinto= sintoma.objects.filter(nombre__startswith=l).values('nombre','id')
    print lista_sinto
    paginator = Paginator(lista_sinto, 1)
    try:
        page = int(pagina)
    except ValueError:
        page = 1
    try:
        sinto = paginator.page(page)
    except (EmptyPage, InvalidPage):
        sinto = paginator.page(paginator.num_pages)
    alfab = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    ctx={'sintoma':sinto,"abc":alfab,'seccion':"sintomas"}
    return render_to_response('glosario/sintomas_ordenadas.html',ctx,context_instance=RequestContext(request)) 
def ver_sintoma(request,id):
    id_sintoma = int(id)
    try:   
        sinto = sintoma.objects.filter(id__exact=id_sintoma)
        for x in sinto:
            sintoma_id=x.id
        sintomas = enfermedad.sintomas
        enfer=enfermedad.objects.filter(sintomas=sintoma_id)
        ctx = {'sintoma':sinto,'id_sintoma':id_sintoma,'enfermedad_rel':enfer}
        return render_to_response('glosario/ver_sintoma.html',ctx,context_instance=RequestContext(request))
    except Exception, e:
        mensaje = "Lo lamento pero este sintoma no existe."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
def enfermedades_view_ordenado_alfabeto(request,letra,pagina):
    l = str(letra)
    enfer = None
    lista_enfer = enfermedad.objects.filter(nombre__startswith=l).values('nombre','id')
    paginator = Paginator(lista_enfer, 2)
    try:
        page = int(pagina)
    except ValueError:
        page = 1
    try:
        enfer = paginator.page(page)
    except (EmptyPage, InvalidPage):
        enfer = paginator.page(paginator.num_pages)
    alfab = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    ctx = {"enfermedad": enfer,"abc":alfab,'seccion':"enfermedad",'l':l}
    return render_to_response('glosario/enfermedades_ordenadas.html',ctx,context_instance=RequestContext(request)) 

def ver_enfermedad(request,id):
    id_enfermedad = int(id)
    try:   
        enfe = enfermedad.objects.filter(id__exact=id_enfermedad)
        mas = []
        enferm = [] 
        enferm2 = []
        dic = {}
        for z in enfe:
            masi = z.masinfo
            enfe_id = z.id
            masinf = masi.split(',')
            try:
                for y in masinf:
                    masinf2 = y.split(';')
                    dic = {'titulo':masinf2[0],'contenido':masinf2[1]}
                    mas.append(dic)
            except Exception, e:
                mas = []
        sinto=sintoma.objects.filter(enfermedad=id_enfermedad)
        medicos = userDoctor.objects.filter(enfermedad_rel=enfe_id)
        print medicos
        for x in sinto:
            id_sintoma = x.id
            enfer = enfermedad.objects.filter(sintomas=id_sintoma)
            for c in enfer:
                if c not in enferm2:
                    enferm2.append(c)
    
        ctx = {'enfermedad':enfe,'masinfo':mas,'id_enfermedad':id_enfermedad,'sintomas_rel':sinto,'enfermedades_rel':enferm2,'medicos_rel':medicos}
        return render_to_response('glosario/ver_enfermedad.html',ctx,context_instance=RequestContext(request))
    except Exception, e:
        mensaje = "Lo lamento pero esta enfermedad no existe."
        ctx = {"mensaje":mensaje,'tipo':"error"}
        return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))



