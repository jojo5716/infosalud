from infosalud.apps.enfermedades.models import sintoma,enfermedad,glosario,pruebas_medicas,medicamentos
from django.contrib import admin

admin.site.register(sintoma)
admin.site.register(enfermedad)
admin.site.register(glosario)
admin.site.register(pruebas_medicas)
admin.site.register(medicamentos)
