from django.contrib import admin
from infosalud.apps.guias.models import estados,ciudades, municipios, guia_centros,especialidades,guia_plantas_curativas,categoria_plantas_medicinales

admin.site.register(estados)
admin.site.register(ciudades)
admin.site.register(municipios)
class centrosAdmin(admin.ModelAdmin):
	list_display = ('nombre','municipio')
	class Media:
		js = ('/media/js/tiny_mce/tiny_mce.js','/media/js/tiny_mce/textareas.js')  
admin.site.register(guia_centros,centrosAdmin)
admin.site.register(especialidades)
admin.site.register(guia_plantas_curativas)
admin.site.register(categoria_plantas_medicinales)