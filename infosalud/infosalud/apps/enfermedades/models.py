from django.db import models

# Create your models here.


#para sintoma no existe enfermedad
class sintoma(models.Model):
	nombre 		= models.CharField(max_length=200)
	definicion	= models.TextField(max_length=500)
	status  	= models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "sintoma"
		verbose_name_plural  = "Sintomas"


#para enfermedad si existe sintoma, arriba ya se encuentra
class enfermedad(models.Model):
	nombre 			= models.CharField(max_length=200)
	definicion		= models.TextField(max_length=500,verbose_name='definicion',blank=True)
	sintomas 		= models.ManyToManyField(sintoma)
	status  		= models.BooleanField(default=True)
	masinfo			= models.TextField(blank=True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ('nombre',)
		verbose_name = "enfermedad"
		verbose_name_plural = "enfermedades"

class glosario(models.Model):
	nombre = models.CharField(max_length=200)
	definicion = models.TextField(max_length=500)

	def __unicode__(self):
		return self.nombre
class pruebas_medicas(models.Model):
	nombre = models.CharField(max_length=200)
	info   = models.TextField(blank=True)
	Enfermedades = models.ManyToManyField(enfermedad)
	status = models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre

class medicamentos(models.Model):
	nombre = models.CharField(max_length=200)
	definicion = models.TextField(max_length=500)
	info   = models.TextField(blank=True)
	enfermedades = models.ManyToManyField(enfermedad)
	status = models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre
