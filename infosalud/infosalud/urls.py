from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^',include('infosalud.apps.home.urls')),
	url(r'^',include('infosalud.apps.notice.urls')),
    url(r'^',include('infosalud.apps.security.urls')),
    url(r'^',include('infosalud.apps.buscador.urls')),
    url(r'^',include('infosalud.apps.enfermedades.urls')),
    url(r'^',include('infosalud.apps.guias.urls')),

	url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
