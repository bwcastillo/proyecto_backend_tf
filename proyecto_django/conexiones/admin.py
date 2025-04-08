from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Organismo, Medida, Reporte, Cumplimiento, Indicador, UsuarioPerfil

# Inline para el perfil extendido
class UsuarioPerfilInline(admin.StackedInline):
    model = UsuarioPerfil
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'

# Admin personalizado para User
class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioPerfilInline,)

# Desregistrar y registrar de nuevo el modelo User con el inline incluido
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registrar otros modelos si quieres
admin.site.register(Organismo)
admin.site.register(Medida)
admin.site.register(Reporte)
admin.site.register(Cumplimiento)
admin.site.register(Indicador)
