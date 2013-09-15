__author__ = 'alex'
from django.contrib import admin
from infosalud.apps.security.models import userDoctor,userProfile, horariosMedico,Post,NoticiaMedico,RecetaMedico,noticias_medicos_ip,mensajes_medicos,envio_emails

admin.site.register(userDoctor)
admin.site.register(userProfile)
admin.site.register(horariosMedico)
admin.site.register(Post)
admin.site.register(NoticiaMedico)
admin.site.register(RecetaMedico)
admin.site.register(noticias_medicos_ip)
admin.site.register(mensajes_medicos)
admin.site.register(envio_emails)
