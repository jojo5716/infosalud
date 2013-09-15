from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from infosalud.apps.enfermedades.models import enfermedad
from infosalud.apps.guias.models import especialidades, guia_centros,estados,ciudades, municipios 
from infosalud.apps.notice.models import categorias_noticias,categorias_recetas,newsletter
from django.core.mail import EmailMultiAlternatives, send_mail

GENDER_CHOICES = (
    ('M', 'Hombre'),
    ('F', 'Mujer'),
    )

"""
@alexjs88
Se liga la clase User y se le agregan campos adiciionales
"""


class userProfile(models.Model):

    def image_path(self,filename):
        url = "MultimediaData/Users/Standard/%s/ImageProfile/%s"%(self.user,str(filename))
        return url

    user                =   models.OneToOneField(User)
    photo               =   models.ImageField(upload_to = image_path,null=True,blank=True)
    fechaNacimiento     =   models.DateField(null=True,blank=True)
    gender              =   models.CharField(max_length=1,choices=GENDER_CHOICES, help_text= "Hombre o Mujer",null=True,blank=True)
    activationKey       =   models.CharField(max_length=200,null=True,blank=True)
    keyExpires          =   models.DateTimeField(null=True,blank=True)
    receiveNews         =   models.BooleanField(default=False)
    receiveInfo         =   models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name        =   " Usuario Estandard "
        verbose_name_plural =   " Usuarios Estandard "

"""
@alexjs88
Se liga la clase usuario y se agregan campos adicionales
"""
class userDoctor(models.Model):

    def image_path(self,filename):
        url = "MultimediaData/Users/Doctor/%s/ImageProfile/%s"%(self.user,str(filename))
        return url

    user                =   models.OneToOneField(User)
    photo               =   models.ImageField(upload_to = image_path)
    fechaNacimiento     =   models.DateField()
    gender              =   models.CharField(max_length=1,choices=GENDER_CHOICES, help_text= "Hombre o Mujer")
    numLicence          =   models.IntegerField()
    university          =   models.CharField(max_length=200,help_text="Nombre de la Universidad Perteneciente ")
    especialidad        =   models.ManyToManyField(especialidades,blank=True,null=True,help_text="Puedes elegir varias especialidades manteniendo  la tecla CONTROL de tu teclado para poder seleccionar varios y tambien para deseleccionar.")
    estado              =   models.ForeignKey(estados)
    municipio           =   models.ForeignKey(municipios)
    dni                 =   models.CharField(max_length=8)
    status              =   models.BooleanField(default=False)
    activationKey       =   models.CharField(max_length=200,null=True,blank=True)
    keyExpires          =   models.DateTimeField(null=True,blank=True)
    receiveNews         =   models.BooleanField(default=False)
    receiveInfo         =   models.BooleanField(default=False)
    enfermedad_rel      =   models.ManyToManyField(enfermedad,blank=True,null=True,help_text="Puedes elegir varias enfermedades manteniendo  la tecla CONTROL de tu teclado para poder seleccionar varios y tambien para deseleccionar.")

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name        =   " Usuario tipo Doctor "
        verbose_name_plural =   " Usuarios Tipo Doctor "
        unique_together = ('dni','numLicence')


'''
@jojo5717
Creamos una tabla para guardar los horarios de los medicos, precios, direccion...
'''
class horariosMedico(models.Model):
    user                =       models.OneToOneField(User)
    horario             =       models.TextField(verbose_name='horarios',blank=True)
    direccion           =       models.TextField(verbose_name='direccion',blank=True)
    precios             =       models.TextField(verbose_name='precios',blank=True)
    tlf                 =       models.CharField(max_length=20,null=True,blank=True)
    horario_act         =       models.BooleanField(default=False)
    direccion_act       =       models.BooleanField(default=False)
    precios_act         =       models.BooleanField(default=False)
    tlf_act             =       models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username
"""
@jojo5717
Se verifica que tipo de perfil (usuario /medico) es el que se esta visitando
"""
def tipo_perfil(id_visitante):
    usuario = None
    try:
        usuario = userDoctor.objects.get(user_id__exact=int(id_visitante))
        if usuario != None:
            if usuario.status:
                tipo ="medico"
                return tipo
            else:
                return None
    except Exception, e:
        print "no coinciden los perfiles (doctor)"
        try:
            usuario = userProfile.objects.get(user_id__exact=int(id_visitante))
            if usuario!= None:
                tipo = "usuario"
                return tipo
            else:
                return None
        except Exception, e:
            print "No coinciden  los perfiles (usuario)"
            return None

"""
@jojo5717
Se crea un modelo para guardar los post de los medicos
"""
class Post(models.Model):
    user = models.ForeignKey(User)
    post = models.CharField(max_length=140,null=True,blank=True)
    fecha_publicacion = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "Usuario: "+self.user.username + " Post: "+self.post

"""
@jojo5717
Se crea un modelo para guardar noticias de medicos.
"""
class NoticiaMedico(models.Model):
    user = models.ForeignKey(User)
    titulo = models.CharField(max_length=140,null=True,blank=True)
    noticia = models.TextField(verbose_name='noticias',blank=True)
    categoria = models.ForeignKey(categorias_noticias)
    fecha_publicacion = models.DateTimeField(auto_now=True)
    n_votos = models.IntegerField(default=0,blank=True)
    m_votos = models.FloatField(default=0.0,blank=True)

    def __unicode__(self):
        return self.user.username + "--> " + self.titulo
    """
@jojo5717
Se crea un modelo para guardar recetas de medicos.
"""
class RecetaMedico(models.Model):
    user = models.ForeignKey(User)
    titulo = models.CharField(max_length=140,null=True,blank=True)
    ingredientes = models.TextField(verbose_name='ingredientes',blank=True)
    preparacion = models.TextField(verbose_name='preparacion',blank=True)
    tiempo =models.CharField(max_length=10,null=True,blank=True,help_text="Escribe un aproximado del tiempo que se necesita para preparar la receta.")
    porcion = models.CharField(max_length=10,null=True,blank=True,help_text="Escribe un aproximado de las porciones de comida para esta receta.Ejemplo: 1,3,4, 2-3 , 1-4, 1-2 ")
    categoria = models.ForeignKey(categorias_recetas)
    fecha_publicacion = models.DateTimeField(auto_now=True)
    n_votos = models.IntegerField(default=0,blank=True)
    imagen = models.ImageField(upload_to='recetas',verbose_name='Imagen',blank=True)
    def __unicode__(self):
        return self.user.username + "--> " + self.titulo
class noticias_medicos_ip(models.Model):
    noticia_id = models.IntegerField(default=0,blank=True)
    noticia_ip = models.CharField(max_length=40,blank=True)
    def __unicode__(self):
        return self.noticia_ip + "--> "+self.noticia_id
class recetas_medicos_ip(models.Model):
    receta_id = models.IntegerField(default=0,blank=True)
    receta_ip = models.CharField(max_length=40,blank=True)
    def __unicode__(self):
        return self.receta_ip + "--> "+self.receta_id

class mensajes_medicos(models.Model):
    autor = models.ForeignKey(User,related_name="message_from")
    medico = models.ForeignKey(User,related_name="message_to")
    titulo = models.CharField(max_length=140,null=True,blank=True)
    mensaje = models.TextField(verbose_name='mensaje',blank=True,max_length=300)
    leido = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(auto_now=True,editable=False)
    class Meta:
        verbose_name = _(u'mensaje')
        verbose_name_plural = _(u'mensajes')

    def __unicode__(self):
        return self.autor.username + " a enviado un mensaje a " + self.medico.username
class envio_emails(models.Model):
    titulo = models.CharField(max_length=140)
    contenido = models.TextField(verbose_name='mensaje',blank=True,max_length=300)
    imagen = models.ImageField(upload_to='envio_emails',verbose_name='Imagen',blank=True)

    def save(self):
            try:
                super(envio_emails, self).save()
                u_emails=[]
                usuario = newsletter.objects.all()
                for x in usuario:
                    emails = User.objects.filter(pk=x.usuario_id)
                    for y in emails:
                        if y not in u_emails:
                            u_emails.append(y.email)
                print u_emails
                subject = self.titulo
                from_email ='from@server.com'
                to=u_emails
                text_content = ''
                html_content = '<div style="color:#3D7489; font-size:25px; text-align:center; font-weight:bold;">%s</div><br/><div style="color:#E36F26; text-align:center; font-size:38px; font-weight:bold;">%s</div><br/><a href="http://www.infosalud.co.ve/media/%s/"><img src="http://infosalud.co.ve/media/%s/" style="margin-left:75px; max-width:500px; max-height:600px;"/></a> <br/><br/><br/> <p>Si usted no desea seguir recibiendo emails por parte de InfoSalud, le recordamos que puede ir a su perfil dentro de nuestra web <a href="www.infosalud.co.ve">www.infosalud.co.ve</a> y desactivar la casilla de Newsletter.<p/>'%(self.titulo,self.contenido,self.imagen,self.imagen)
                msg = EmailMultiAlternatives(subject,text_content,from_email,to)
                msg.attach_alternative(html_content,"text/html")
                msg.send()
            except Exception, e:
                print "no se pudo enviar los emails"
    def __unicode__(self):
        return self.titulo


