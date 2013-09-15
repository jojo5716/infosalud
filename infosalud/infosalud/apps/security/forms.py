__author__ = 'alex'
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from infosalud.apps.notice.models import categorias_noticias
from infosalud.apps.guias.models import estados
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username        = forms.CharField(label=(u'User Name'),widget=forms.TextInput(attrs={'required':'True','placeholder':'Nombre de usuario'}))
    password        = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False,attrs={'required':'True','placeholder':'Contraseña'}))

class RegistrationStandardForm(forms.Form):

    GENDER_CHOICES = (
    ('M', 'Hombre'),
    ('F', 'Mujer'),
    )

    username = forms.CharField(label=(u'Nombre de Usuario'),widget=forms.TextInput(attrs={'required':'True','placeholder':'Nombre de usuario'}))
    email = forms.EmailField(label=(u'Email'),widget=forms.TextInput(attrs={'required':'True','placeholder':'Tu email'}))
    password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False,attrs={'required':'True'}))
    password1 = forms.CharField(label=(u'Verifica tu Password'),widget=forms.PasswordInput(render_value=False,attrs={'required':'True'}))
    gender = forms.ChoiceField(widget = forms.Select(attrs={'class':'form-login'}),choices = GENDER_CHOICES, initial='1', required = True,)
    newsletter = forms.BooleanField(required=False,initial=True)
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Correo electronico ya se encuentra registrado')
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Ya existe este usuario,')

class RegistrationDoctorForm(forms.Form):
    GENDER_CHOICES = (
    ('M', 'Hombre'),
    ('F', 'Mujer'),
    )
    username = forms.CharField(label=(u'User Name'),widget=forms.TextInput(attrs={'placeholder':'nombre de usuario'}))
    nombre = forms.CharField(label=(u'Nombre'),widget=forms.TextInput(attrs={'placeholder':'Nombre','required':'True'}))
    apellido = forms.CharField(label=(u'Apellido'),widget=forms.TextInput(attrs={'placeholder':'Apellido','required':'True'}))
    cedula = forms.CharField(label=(u'cedula'),widget=forms.TextInput(attrs={'placeholder':'Cedula de Identidad','required':'True'}))
    email = forms.EmailField(label=(u'Email'),widget=forms.TextInput(attrs={'required':'True','placeholder':'Tu email'}))
    especialidad = forms.CharField(label=(u'especialidad'),widget=forms.TextInput(attrs={'placeholder':'especialidad','required':'True'}))
    universidad = forms.CharField(label=(u'universidad'),widget=forms.TextInput(attrs={'placeholder':'universidad','required':'True'}))
    gender = forms.ChoiceField(widget = forms.Select(attrs={'class':'form-login'}),choices = GENDER_CHOICES, initial='1', required = True,)
    graduacion = forms.CharField(label=(u'Graduacion'),widget=forms.TextInput(attrs={'placeholder':'universidad','required':'True'}))
    numLicence = forms.CharField(label=(u'licencia'),widget=forms.TextInput(attrs={'placeholder':'Numero de licencia','required':'True'}))
    password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False,attrs={'placeholder':'Clave de acceso','required':'True'}))
    password1 = forms.CharField(label=(u'Verify Password'),widget=forms.PasswordInput(render_value=False,attrs={'placeholder':'Confirmar clave de acceso','required':'True'}))
    newsletter = forms.BooleanField(required=False) 
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Correo electronico ya se encuentra registrado')
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Ya existe este usuario,')

    def clean_password1(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('Las claves no coinciden')
        return self.cleaned_data
#Formulario para editar (email) perfil medico.
class edit_perfil_medico(forms.Form):

    email = forms.EmailField(label=(u'email'),widget=forms.TextInput(attrs={'placeholder':'email','required':'True'}))
    photo = forms.FileField()
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Correo electronico ya se encuentra registrado')
#Formulario para editar (password) perfil medico.
class editar_contrasena(forms.Form):
    old_password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False,attrs={'placeholder':'Actual clave','required':'True'}))
    new_password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False,attrs={'placeholder':'Nueva clave','required':'True'}))
    again_password = forms.CharField(label=(u'Verify Password'),widget=forms.PasswordInput(render_value=False,attrs={'placeholder':'Repite la clave','required':'True'}))

class edit_consultorio_medico(forms.Form):
    

    direccion  = forms.CharField(label=(u'Direccion'),widget=forms.Textarea(attrs={'placeholder':'Escribe la direccion de tu consultorio','required':'True'}))
    telefono = forms.CharField(label=(u'Telefono'),widget=forms.TextInput(attrs={'placeholder':'Telefono','required':'True'}))
    horarios = forms.CharField(label=(u'Horarios'),widget=forms.Textarea(attrs={'placeholder':'Escribe tus horarios en la cual puedes atiender a tus pacientes.','required':'True'}))
    precios = forms.CharField(label=(u'Precios'),widget=forms.Textarea(attrs={'placeholder':'Escribe una lista de precios correspondientes a tus servicios.','required':'True'}))
    direccion_act = forms.BooleanField(required=False)
    horarios_act = forms.BooleanField(required=False)
    telefono_act = forms.BooleanField(required=False)
    precios_act = forms.BooleanField(required=False)
    
class edit_perfil_usuario(forms.Form):
    email = forms.EmailField(label=(u'email'),widget=forms.TextInput(attrs={'placeholder':'email','required':'True'}))
class edit_newsletter(forms.Form):
    newsletter = forms.BooleanField(required=False)

class Registro_paciente(forms.Form):
    ESTADO_CHOICES = (
        ('aragua','Aragua'),
        ('carabobo','Carabobo'),
        )
    MUNICIPIO_CHOICES = (
        ('maracay','Maracay'),
        ('valencia','Valencia'),
        )
    GENDER_CHOICES = (
        ('M', 'Hombre'),
        ('F', 'Mujer'),
        )
    CIVIL_CHOICES = (
        ('s','Soltero'),
        ('c','Casado'),
        ('d','Divorciado'),
        ('v','Viudo'),
        )
    username = forms.CharField(label=(u'Nombre de Usuario'),widget=forms.TextInput(attrs={'required':'True'}))
    nombre = forms.CharField(label=(u'Nombre de Paciente'),widget=forms.TextInput(attrs={'required':'True'}))
    apellido = forms.CharField(label=(u'Apellido de Paciente'),widget=forms.TextInput(attrs={'required':'True'}))
    dni = forms.CharField(label=(u'Cedula de identidad'),widget=forms.TextInput(attrs={'required':'True'}))
    email = forms.EmailField(label=(u'Email'),widget=forms.TextInput(attrs={'required':'True'}))
    password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False,attrs={'required':'True'}))
    password1 = forms.CharField(label=(u'Verifica tu Password'),widget=forms.PasswordInput(render_value=False,attrs={'required':'True'}))
    gender = forms.ChoiceField(label=(u'Genero'), widget = forms.Select,choices = GENDER_CHOICES, initial='1', required = True,)
    fechaNacimiento = forms.DateField(label=(u'Fecha Nacimiento'), widget=forms.TextInput(attrs={'required':'True'}))
    estado = forms.ChoiceField(label=(u'Estado'), widget = forms.Select,choices = ESTADO_CHOICES, initial='1', required = True,)
    municipio = forms.ChoiceField(label=(u'Municipio'), widget = forms.Select,choices = MUNICIPIO_CHOICES, initial='1', required = True,)
    edoCivil = forms.ChoiceField(label=(u'Estado civil'), widget = forms.Select,choices = CIVIL_CHOICES, initial='1', required = True,)
    tlf_cel = forms.CharField(label=(u'Tlf. Movil'),widget=forms.TextInput(attrs={'required':'True'}))
    tlf_casa = forms.CharField(label=(u'Tlf. Casa'),widget=forms.TextInput(attrs={'required':'True'}))
class PostsMedicos(forms.Form):
    post = forms.CharField(label=(u'Nuevo post'),widget=forms.TextInput(attrs={'placeholder':'Comparte algun estado con los demas usuarios','required':'True'}))

"""
@jojo5717
Se crea un formulario para que los medicos suban sus noticias/recetas
"""  

class NoticiaMedicos(forms.Form):
    titulo = forms.CharField(label=(u'Titulo'),widget=forms.TextInput(attrs={'placeholder':'Escribe un titulo para la noticia','required':'True'}))
    noticia  = forms.CharField(label=(u'Noticia'),widget=forms.Textarea(attrs={'placeholder':'Escribe la noticia','required':'True'}))
class RecetaMedicos(forms.Form):
    titulo = forms.CharField(label=(u'Titulo'),widget=forms.TextInput(attrs={'placeholder':'Escribe un titulo para la noticia','required':'True'}))
    ingredientes  = forms.CharField(label=(u'Ingredientes'),widget=forms.Textarea(attrs={'placeholder':'Escribe los ingredientes','required':'True'}))
    preparacion = forms.CharField(label=(u'Preparacion'),widget=forms.Textarea(attrs={'placeholder':'Escribe los pasos para preparar esta receta','required':'True'}))
    tiempo = forms.CharField(label=(u'Tiempo de preparacion'),widget=forms.TextInput(attrs={'placeholder':'Escribe un aproximado en tiempo de preparacion','required':'True','value':'0'}))
    
class ContactoMedico(forms.Form):
    titulo = forms.CharField(label=(u'Titulo'),widget=forms.TextInput(attrs={'placeholder':'Escribe un titulo para tu mensaje','required':'True'}))
    mensaje = forms.CharField(label=(u'Mensaje'),widget=forms.Textarea(attrs={'placeholder':'Escribe porque estas contactando a este medico.','required':'True'}))
class ReportarMedico(forms.Form):
    mensaje = forms.CharField(label=(u'Mensaje'),widget=forms.Textarea(attrs={'placeholder':'Cuentanos tu experiencia con este medico y porque estas denunciandolo.','required':'True'}))

class responder_mensaje_medico(forms.Form):
    mensaje = forms.CharField(label=(u'Mensaje'),widget=forms.Textarea(attrs={'placeholder':'Escribe tu respuesta al mensaje.','required':'True'}))


