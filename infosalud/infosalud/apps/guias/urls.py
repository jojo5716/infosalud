from django.conf.urls.defaults import patterns,url


urlpatterns = patterns('infosalud.apps.guias.views',
	url(r'^infoguia/$','infoguia_view',name='vista_infoguia'),
	url(r'^especialidades/$','ver_especialidades_view',name='vista_especialidades'),
	url(r'^medicos_estado/(?P<especialidad>.*)/(?P<estado>.*)$','ver_estados_especialidad',name='vista_medicos_especialidades'),
	url(r'^ver_mapa/(?P<especialidad>.*)$','ver_mapa_especialidad',name='vista_menicipios_especialidad'),
	url(r'^plantas/curativas/(?P<pagina>.*)/$','ver_plantas_curativas',name='vista_plantas_curativas'),
	url(r'^planta/(?P<id>.*)/$','ver_plantas_curativas_id',name='vista_plantas_curativas_nombre'),
	url(r'^plantas/seccion/(?P<tag>.*)/(?P<pagina>.*)$','ver_plantas_seccion_tag',name='vista_plantas_curativas_tag'),
)