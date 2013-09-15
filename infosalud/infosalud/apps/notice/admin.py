

from infosalud.apps.notice.models import noticia, banner, categorias_noticias,categorias_recetas, recetas, noticias_ip,newsletter,MultipleChoice,MultipleChoiceAnswer,Quiz,UserResponse


class noticiaAdmin(admin.ModelAdmin):
	list_display = ('titulo','autor')
	class Media:
		js = ('/media/js/tiny_mce/tiny_mce.js','/media/js/tiny_mce/textareas.js')  
class recetaAdmin(admin.ModelAdmin):
	list_display = ('titulo','autor')
admin.site.register(noticia,noticiaAdmin)
admin.site.register(banner)
admin.site.register(categorias_noticias)
admin.site.register(categorias_recetas)
admin.site.register(recetas,recetaAdmin)
admin.site.register(noticias_ip)
admin.site.register(newsletter)
admin.site.register(MultipleChoice)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(Quiz)
admin.site.register(UserResponse)
