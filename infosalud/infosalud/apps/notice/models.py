#encoding:utf-8
from django.db import models

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.exceptions import ValidationError

from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db.models import permalink
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords_html

class newsletter(models.Model):
    usuario = models.ForeignKey(User)
    def __unicode__(self):
        return str(self.usuario)

 
class noticia(models.Model):
	titulo = models.CharField(max_length=200,blank=True)
	autor = models.ForeignKey(User)
	imagen = models.ImageField(upload_to='noticias',verbose_name='Imagen',blank=True)
	noticia = models.TextField(verbose_name='Noticia',blank=True)
	tiempo_registro = models.DateTimeField(auto_now=True,blank=True)
	n_votos = models.IntegerField(default=0,blank=True)
	m_votos = models.FloatField(default=0.0,blank=True)
	categoria = models.ForeignKey('categorias_noticias')
	media = models.FloatField(default=0.0,blank=True)

	def __unicode__(self):
		return self.titulo


	def clean(self):
		if len(self.titulo)<2:
			print len(self.titulo)
			raise ValidationError('No es valido')
		
		
class banner(models.Model):
	titulo = models.CharField(max_length=140)
	imagen = models.ImageField(upload_to='banner',verbose_name='Imagen')
	noticia = models.TextField(verbose_name='Banner')
	tiempo_registro = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.titulo

class categorias_noticias(models.Model):
	categoria = models.CharField(max_length=140)

	def __unicode__(self):
		return self.categoria
class categorias_recetas(models.Model):
	categoria = models.CharField(max_length=140)
	def __unicode__(self):
		return self.categoria

	def __unicode__(self):
		return self.categoria

class noticias_ip(models.Model):
	noticia_id = models.IntegerField(default=0,blank=True)
	noticia_ip = models.CharField(max_length=40,blank=True)

	def __unicode__(self):
		return "Noticia: "+str(self.noticia_id)+" IP: "+ str(self.noticia_ip)
class recetas_ip(models.Model):
	recetas_id = models.IntegerField(default=0,blank=True)
	recetas_ip = models.CharField(max_length=40,blank=True)

	def __unicode__(self):
		return "Receta: "+str(self.recetas_id)+" IP: "+ str(self.recetas_ip)
class recetas(models.Model):
	titulo = models.CharField(max_length=200,blank=False)
	autor = models.ForeignKey(User)
	imagen = models.ImageField(upload_to='recetas',verbose_name='Imagen')
	preparacion = models.TextField(verbose_name='Preparacion',help_text="Escribe los pasos necesarios para realizar esta receta seguida por comas ( , ). Ejemplo: Se cortan los tomates, Se Corta el pollo, Etc...")
	ingredientes = models.TextField(verbose_name="Ingredientes",help_text="Escribe los ingredientes necesarios para preparar esta receta seguida por comas ( , ). Ejemplo: Sal, Pimienta, 5 tomates, 1/4 de tasa con harina, etc... ")
	tiempo_registro = models.DateTimeField(auto_now=True)
	n_votos = models.IntegerField(default=0,blank=True)
	m_votos = models.FloatField(default=0.0,blank=True)
	categoria = models.ForeignKey('categorias_recetas')
	media = models.FloatField(default=0.0,blank=True)
	tiempo =models.CharField(max_length=10,null=True,help_text="Escribe un aproximado del tiempo que se necesita para preparar la receta.")
	porcion = models.CharField(max_length=10,null=True,help_text="Escribe un aproximado de las porciones de comida para esta receta.Ejemplo: 1,3,4, 2-3 , 1-4, 1-2 ")
	enviar = models.BooleanField(default=False)
	def __unicode__(self):
		return self.titulo

	def save(self):
		try:
			super(recetas, self).save()
			if self.enviar:
				u_emails=[]
				usuario = newsletter.objects.all()
				for x in usuario:
					emails = User.objects.filter(pk=x.usuario_id)
					for y in emails:
						if y not in u_emails:
							u_emails.append(y.email)
				print u_emails
				subject = "Nueva receta de InfoSalud"
				from_email ='from@server.com'
				to=u_emails
				text_content = ''
				
				html_content = '<div style="color:#3D7489; font-size:25px; text-align:center; font-weight:bold;">InfoSalud ha creado una nueva receta que seguro te encantara!</div><br/><div style="color:#E36F26; text-align:center; font-size:38px; font-weight:bold;"><a href="www.infosalud.co.ve/receta/%s/">%s</a></div><br/><a href="www.infosalud.co.ve/receta/%s/"><img src="http://infosalud.co.ve/media/%s" style="border-radius:999px; margin-left:75px; width:200px; height:200px;"/></a> <br/><br/><br/> <p>Si usted no desea seguir recibiendo emails por parte de InfoSalud, le recordamos que puede ir a su perfil dentro de nuestra web <a href="www.infosalud.co.ve">www.infosalud.co.ve</a> y desactivar la casilla de Newsletter.<p/>'%(self.id,self.titulo,self.id,self.imagen)
				msg = EmailMultiAlternatives(subject,text_content,from_email,to)
				msg.attach_alternative(html_content,"text/html")
				msg.send()

		except Exception, e:
			print "no se pudo enviar los email de la nueva receta."



class MultipleChoiceAnswer(models.Model):
	'''A multichoice answer.'''
	answer = models.TextField(_('answer'))

	def __unicode__(self):
		return u"%s" % truncatewords_html(self.answer, 10)


class MultipleChoice(models.Model):
	'''Multiple choice question with answer choices.'''
	question = models.TextField(_('question'))
	slug = models.SlugField(_('slug'))
	choices = models.ManyToManyField(MultipleChoiceAnswer)
	correct_answer = models.ManyToManyField(MultipleChoiceAnswer, related_name="correct", blank=True) #can have more than 1 correct answer, can be blank
	explanation = models.TextField(_('Explain your answer'), blank=True)

	def __unicode__(self):
		return u"%s" % truncatewords_html(self.question, 10)

        @permalink
        def get_absolute_url(self):
		return ('quiz.views.question', [self.pk, self.slug])


class Quiz(models.Model):
	'''A quiz template.'''
	STATUS_CHOICES = (
		(1, _('Draft')),
		(2, _('Public')),
		(3, _('Close')),
	)

	FEEDBACK_CHOICES = (
		(1, _('At the end of the quiz')),
		(2, _('After each question')),
		(3, _('Don\'t disclose')),
	)

	TYPE_CHOICES = (
		(1, _('After Lecture')),
		(2, _('Assessment')),
		(3, _('Exam')),
	)
	NO_OF_TAKES_PER_MONTH_PER_USER = 3
	NO_OF_INSTANCES_PER_MONTH_PER_SETTER = 20
	setter = models.ForeignKey(User, related_name='setter')
	title = models.CharField(_('title'), max_length=100)
	slug = models.SlugField(_('slug'))
	description = models.TextField(_('description'), blank=True, null=True)	
	status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
	type = models.IntegerField(_('quiz type'), choices=TYPE_CHOICES, default=2)
	questions = models.ManyToManyField(MultipleChoice)
	published = models.DateTimeField(_('published'))	
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now_add=True)

	allow_skipping = models.BooleanField(default=False)
	allow_jumping = models.BooleanField(default=False)
	backwards_navigation = models.BooleanField(default=False)
	random_question = models.BooleanField(default=False) # conditional
	feedback = models.IntegerField(_('feedback'), choices=FEEDBACK_CHOICES, default=1)
	multiple_takes = models.BooleanField(default=False) # conditional
	# default must be global setting
	no_of_takes_per_month = models.IntegerField(_('no. of times this quiz can be taken by the candidate per month'),
						    default=NO_OF_TAKES_PER_MONTH_PER_USER)
	no_of_instances_per_month = models.IntegerField(_('no. of times this quiz can be taken by the candidate per month'),
						    default=NO_OF_INSTANCES_PER_MONTH_PER_SETTER)

	class Meta:
		verbose_name = _('quiz')
		verbose_name_plural = _('quizzes')
		db_table = 'quizzes'
		ordering = ('-published',)

	def __unicode__(self):
		return u"%s" % self.title

	@property
	def question_count(self):
		return len(self.questions.all())

	def get_question(self, id):
		return self.questions.all()[id]

	@property
	def get_instances(self):
		return QuizInstance.objects.filter(quiz=self)

	@property
	def get_completed_instances(self):
		return this.get_instances.filter(complete=True)

	@property
	def get_instances_last_month(self):
		return self.get_instances_since_month(1)

	def get_instances_since_month(self, no_of_months=1, user=None):
		instances = this.get_completed_instances.filter(quiz_taken__gt=date.today() - relativedelta(months=no_of_months))
		if user: return instances.filter(taker=user)
		else: return instances


class QuizInstance(models.Model):
	'''A combination of user response and a quiz template.'''
	taker = models.ForeignKey(User)
	quiz = models.ForeignKey(Quiz)
	quiz_taken = models.DateTimeField(_('quiz taken'), auto_now_add=True)
	score = models.IntegerField(default=0)
	complete = models.BooleanField(default=False)
	# prevent from setting score in the frontend to avoid tampering
	def __setattr__(self, name, value):
		if name == 'score':
			if getattr(self, 'score', None):
				if getattr(self, 'score') != 0 and getattr(self, 'score') != value:
					print "Verga que loco"
		super(QuizInstance, self).__setattr__(name, value)

	def __unicode__(self):
		return u"%s, taken by %s on %s" % (self.quiz, self.taker, self.quiz_taken.strftime("%A, %d %B %Y %I:%M%p"))

	@property
	def get_responses(self):
		return UserResponse.objects.filter(quiz_instance=self).all()


class UserResponse(models.Model):
	'''User response to a single question.'''
	quiz_instance = models.ForeignKey(QuizInstance)
	question = models.ForeignKey(MultipleChoice)
	response = models.ManyToManyField(MultipleChoiceAnswer, related_name="response")
	time_taken = models.DateTimeField(_('When was the question posed'), auto_now_add=True)
	time_taken_delta = models.DateTimeField(_('When was the question answered'), blank=True)

	def __unicode__(self):
		return u"Response to %s for %s" % (self.question, self.quiz_instance)
	@property
	def is_correct(self):
		return self.question.correct_answer.all()==self.response.all()