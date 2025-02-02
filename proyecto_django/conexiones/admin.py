from django.contrib import admin
from .models import Organismo, Medida, Reporte, Cumplimiento, Usuario, Indicador


# Register your models here.
admin.site.register(Organismo)
admin.site.register(Medida)
admin.site.register(Reporte)
admin.site.register(Cumplimiento)
admin.site.register(Usuario)
admin.site.register(Indicador)
