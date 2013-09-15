__author__ = 'jojo5716'

from django.conf.urls.defaults import patterns,url


urlpatterns = patterns('infosalud.apps.buscador.views',
    url(r'^buscar/$','search',name='vista_buscar'),
)