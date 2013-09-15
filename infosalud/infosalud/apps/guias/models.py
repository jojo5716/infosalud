# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.
class estados(models.Model):
	nombre 	=	models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre


class ciudades(models.Model):
	nombre		= 	models.CharField(max_length=200)
	estado 		= 	models.OneToOneField(estados)
	def __unicode__(self):
		return self.nombre

class municipios(models.Model):
	nombre 		= 	models.CharField(max_length=200)
	estados 	= 	models.ForeignKey(estados)
	def __unicode__(self):
		return self.nombre 


class guia_centros(models.Model):
	nombre 			= 	models.CharField(max_length=100)
	municipio 		= 	models.ForeignKey(municipios)
	direccion 		= 	models.TextField(help_text="Indique la direccion del centro de salud.")
	servicios 		= 	models.TextField(help_text="Indique los servicios que presta este centro.")
	observaciones 	= 	models.TextField(help_text="Indique alguna informacion adicional, observaciones, etc.",blank=True)
	horarios 		= 	models.TextField(help_text="Indique los horario que tiene el servicio separados por comas ( , ) y  con el formato de ejmplo: Lun-Vie 06:00am - 12:00pm / 02:00pm - 06:00am , Sab - Dom 07:00am - 12:00pm / 02:00pm - 07:00pm")
	especialidades	=	models.TextField(help_text="Indique las especialidades de los medicos que se pueden encontrar en este centro.")
	def __unicode__(self):
		return self.nombre 

class especialidades(models.Model):
	nombre 	= 	models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre
class categoria_plantas_medicinales(models.Model):
	nombre = models.CharField(max_length=100)
	def __unicode__(self):
		return self.nombre

class guia_plantas_curativas(models.Model):
	nombre 		=	models.CharField(max_length=100)
	cultivo		=	models.TextField(help_text="Indique como es el cultivo de esta planta.")
	propiedades	=	models.TextField(help_text="Indique las propiedades beneficas que tiene esta guia_plantas_curativas.")
	formas_uso	=	models.TextField(help_text="Indique en que forma se debe usar esta planta para aprovechar sus propiedades curativas.")
	Imagen 		= 	models.ImageField(upload_to='plantas',verbose_name='Imagen',blank=True)
	tags 		= 	models.ManyToManyField(categoria_plantas_medicinales)

	def __unicode__(self):
		return self.nombre