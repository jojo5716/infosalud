from django.shortcuts import render_to_response
from django.template import RequestContext
from infosalud.apps.guias.models import especialidades, municipios ,guia_plantas_curativas,categoria_plantas_medicinales
from infosalud.apps.security.models import userDoctor
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def infoguia_view(request):
    return render_to_response('guia/infoguia.html',context_instance=RequestContext(request))

def ver_especialidades_view(request):
	espe = especialidades.objects.all()
	ctx = {'especialidad':espe}
	return render_to_response('guia/especialidades_medicos.html',ctx,context_instance=RequestContext(request)) 

def ver_mapa_especialidad(request,especialidad):
	espe = int(especialidad)
	medico = userDoctor.objects.filter(especialidad=espe)
	ctx = {'medicos':medico,'image':'venezuela.gif'}
	return render_to_response('guia/municipios_especialidad.html',ctx,context_instance=RequestContext(request))

def ver_estados_especialidad(request,especialidad,estado):
	espe = int(especialidad)
	esta = int(estado)
	medico = userDoctor.objects.filter(especialidad=espe,estado=esta)
	ctx = {'medicos':medico,'image':'municipios.jpg'}
	return render_to_response('guia/municipios_especialidad.html',ctx,context_instance=RequestContext(request))

def ver_medicos_especialidad(request,especialidad):
	espe = int(especialidad)
	medico = userDoctor.objects.filter(especialidad=espe)
	ctx = {'medicos':medico}
	return render_to_response('guia/medicos_especialidad.html',ctx,context_instance=RequestContext(request)) 

def ver_plantas_curativas(request,pagina):
	plantas= None
	plantas = guia_plantas_curativas.objects.all().order_by('-nombre')
	categorias = categoria_plantas_medicinales.objects.all()
	print categorias

	paginator = Paginator(plantas, 6)
	try:
		page = int(pagina)
	except ValueError:
		page = 1
	try:
		plan = paginator.page(page)
	except (EmptyPage, InvalidPage):
		plan = paginator.page(paginator.num_pages)    
	ctx = {'plantas':plan,'tags':categorias}
	return render_to_response('guia/plantas_curativas.html',ctx,context_instance=RequestContext(request)) 

def ver_plantas_curativas_id(request,id):
	try:
		plantas = guia_plantas_curativas.objects.filter(id__exact=id)
		categorias = categoria_plantas_medicinales.objects.filter(guia_plantas_curativas=id)
		print categorias
		mas = []
		
		for x in plantas:
			f = x.formas_uso
			formas = f.split(',')
			id_planta = x.id
			nombre = x.nombre
			try:
				for y in formas:
					formas2 = y.split(';')
					dic = {'titulo':formas2[0],'contenido':formas2[1]}
					mas.append(dic)
			except Exception, e:
				mas=[]
		
		print id_planta
	except Exception, e:
		mensaje = "No se encontro ningun resultado."
		ctx = {'mensaje':mensaje,'tipo':'error'}
		return render_to_response('mensajes/mensajes.html',ctx,context_instance=RequestContext(request))
	ctx = {'planta':plantas,'formas':mas,'id':id_planta,'tags':categorias,'nombre':nombre}
	return render_to_response('guia/planta.html',ctx,context_instance=RequestContext(request))

def ver_plantas_seccion_tag(request,tag,pagina):
	try:
		plantas_tag = guia_plantas_curativas.objects.filter(tags=tag)
		categorias = categoria_plantas_medicinales.objects.all()
		seccion = categoria_plantas_medicinales.objects.get(pk=tag)
		paginator = Paginator(plantas_tag, 6)
		try:
			page = int(pagina)
		except ValueError:
			page = 1
		try:
			plan = paginator.page(page)
		except (EmptyPage, InvalidPage):
			plan = paginator.page(paginator.num_pages)    
		ctx = {'plantas':plan,'tags':categorias,'seccion':seccion}
		return render_to_response('guia/plantas_seccion.html',ctx,context_instance=RequestContext(request)) 
	except Exception, e:
		raise e
	








