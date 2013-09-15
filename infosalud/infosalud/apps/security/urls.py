__author__ = 'alex'

from django.conf.urls.defaults import patterns,url


urlpatterns = patterns('infosalud.apps.security.views',
    url(r'^registro/select/$','register_selection_view',name='vista_seleccionar_registrar'),
    url(r'^registro/standard/$','register_view',name='vista_registrar'),
    url(r'^registro/doctor/$','register_doctor_view',name='vista_registrar_doctor'),
    url(r'^ver_perfil/(?P<id>.*)$','ver_perfil',name='vista_perfil_usuario'),
    url(r'^verificar/$','verificar_pass',name='verificar_datos_perfil'),
    url(r'^agregar_user/(?P<id>.*)$','agregar_user',name='agregar_usuario'),
    url(r'^crear_paciente/$','crear_user',name='crear_usuario'),
    url(r'^post/(?P<id>.*)$','post_medico',name='post_view'),
    url(r'^noticia_medico/(?P<id>.*)$','noticia_medico',name='noticia_view'),
    url(r'^ver_noticia_medico/(?P<id>.*)$','ver_noticia_medico',name='ver_noticia_view'),
    url(r'^ver_receta_medico/(?P<id>.*)$','ver_receta_medico',name='ver_receta_view'),
    url(r'^receta_medico/(?P<id>.*)$','receta_medico',name='receta_view'),
    url(r'^rate_noti_medico/$','rate_noticias_medicos',name='rate_view_noticias'),
    url(r'^rate_recet_medico/$','rate_recetas_medicos',name='rate_view_recetas'),
    url(r'^contactar_medico/(?P<id>.*)$','contacto_medicos',name='contacto_medicos_view'),
    url(r'^reportar_medicos/(?P<id>.*)$','reportar_medico',name='reportar_medicos_view'),
    url(r'^editar/consultorio/medico/(?P<id>.*)$','editar_consultorio_medico',name='editar_consultorio_medicos_view'),
    url(r'^editar/informacion/medico/(?P<id>.*)$','editar_perfil_medico',name='editar_perfil_medicos_view'),
    url(r'^cuenta/confirmar/(?P<user_name>.*)/(?P<activation_key>.*)/$','confirmAccount',name='activacion_view'),
    url(r'^ver/mensajes/medico/(?P<id>.*)$','ver_mis_mensajes_medico',name='mensaje_medico_view'),
    url(r'^leer/mensaje/medico/(?P<id>.*)/(?P<id_medic>.*)$','leer_mensaje',name='leer_mensaje_view'),

)