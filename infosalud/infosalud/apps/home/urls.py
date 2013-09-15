from django.conf.urls.defaults import patterns,url


urlpatterns = patterns('infosalud.apps.home.views',
	url(r'^$','index_view',name='vista_principal'),
	url(r'^contacto/$','contacto_view',name='vista_contacto'),
    url(r'^logout/$','logout_view',name='vista_logout'),
    url(r'^donar/$','donar',name='vista_logsout'),
)