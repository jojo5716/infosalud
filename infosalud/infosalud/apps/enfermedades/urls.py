from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('infosalud.apps.enfermedades.views',
	url(r'^glosario/pagina/(?P<pagina>.*)/$','glosario_view',name='glosario'),
	url(r'^glosario/letra/(?P<letra>.*)/$','glosario_view_ordenado_alfabeto',name='glosario_orden'),
	url(r'^enfermedad/pagina/(?P<pagina>.*)/$','enfermedades_view',name='all_enfer'),
	url(r'^enfermedad/letra/(?P<letra>.*)/(?P<pagina>.*)/$','enfermedades_view_ordenado_alfabeto',name='enfermedades_orden'),
	url(r'^sintomas/pagina/(?P<pagina>.*)/$','sintomas_view',name='all_sinto'),
	url(r'^sintomas/letra/(?P<letra>.*)/(?P<pagina>.*)/$','sintomas_view_ordenado_alfabeto',name='sintomas_orden'),
	url(r'^ver_enfermedad/(?P<id>.*)/$','ver_enfermedad',name='ver_enfer'),
	url(r'^ver_glosario/(?P<id>.*)/$','ver_glosario',name='ver_glo'),
	url(r'^ver_sintoma/(?P<id>.*)/$','ver_sintoma',name='ver_glo'),


)