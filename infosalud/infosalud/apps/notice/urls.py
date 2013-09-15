from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('infosalud.apps.notice.views',
	url(r'^noticia/(?P<id_n>.*)$','notice_view',name='noticia'),
	url(r'^rate/$','rate_view',name='r_v'),
	url(r'^rateReceta/$','rate_view_recetas',name='r_v_recetas'),
	url(r'^recomendar/$','recomendar_view',name='re_v'),
	url(r'^recomendarR/$','recomendar_receta_view',name='rec_v'),
	url(r'^noticias/pagina/(?P<pagina>.*)/$','all_noticias',name='all_noti'),
	url(r'^recetas/pagina/(?P<pagina>.*)/$','all_recetas',name='all_rece'),
	url(r'^receta/(?P<id_r>.*)/$','recetas_view',name='receta'),
	url(r'^ordenar_noticia/(?P<secc>.*)/(?P<orde>.*)/(?P<pagina>.*)/$','ordenar_noticia',name='ordenar_noticias'),
	url(r'^ordenar_receta/(?P<secc>.*)/(?P<orde>.*)/(?P<pagina>.*)/$','ordenar_receta',name='ordenar_recetas'),


)
