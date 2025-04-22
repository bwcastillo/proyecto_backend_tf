import logging
import os
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Organismo, Medida, Reporte, Cumplimiento, Indicador, UsuarioPerfil, PPDA, PeriodoPPDA

LOG_PATH = os.path.join(settings.BASE_DIR, 'logs', 'proyecto.log')


class UsuarioPerfilInline(admin.StackedInline):
    """
    Permite editar el perfil de usuario desde la página del admin de User.
    """
    model = UsuarioPerfil
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'


class UserAdmin(BaseUserAdmin):
    """
    Agrega el perfil extendido al admin del modelo User.
    """
    inlines = (UsuarioPerfilInline,)


# Reemplaza el admin original del modelo User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Organismo)
class OrganismoAdmin(admin.ModelAdmin):
    """Admin para el modelo Organismo."""
    list_display = ('nombre', 'region')
    search_fields = ('nombre', 'region')


@admin.register(Medida)
class MedidaAdmin(admin.ModelAdmin):
    """Admin para el modelo Medida con validaciones personalizadas."""
    list_display = ('nombre_corto', 'organismo', 'frecuencia', 'regulatoria')
    list_filter = ('frecuencia', 'regulatoria')
    search_fields = ('nombre_corto', 'referencia_pda', 'tipo_medida')

    def save_model(self, request, obj, form, change):
        """
        Valida que si la medida es regulatoria, debe tener frecuencia definida.
        También registra un log con el usuario que realiza el cambio.
        """
        if obj.regulatoria and not obj.frecuencia:
            self.message_user(
                request,
                "Las medidas regulatorias deben tener una frecuencia definida.",
                level='error'
            )
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                f"Medida inválida por usuario {request.user}: regulatoria sin frecuencia")
            return  # evita guardar si no cumple la regla

        obj.modificado_por = request.user
        if not change:
            obj.creado_por = request.user

        super().save_model(request, obj, form, change)


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    """Admin para el modelo Reporte."""
    list_display = ('fecha', 'estado', 'organismo', 'medida')
    list_filter = ('estado', 'fecha')
    search_fields = ('estado',)


@admin.register(Cumplimiento)
class CumplimientoAdmin(admin.ModelAdmin):
    """Admin para el modelo Cumplimiento."""
    list_display = ('medida', 'porcentaje_cumplimiento')
    list_filter = ('porcentaje_cumplimiento',)


@admin.register(Indicador)
class IndicadorAdmin(admin.ModelAdmin):
    """Admin para el modelo Indicador."""
    list_display = ('descripcion',)
    search_fields = ('descripcion', 'formula_calculo', 'medio_verificacion')


@admin.register(PPDA)
class PPDAAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo PPDA.
    Muestra nombre, fecha de inicio y fecha de fin en la vista de lista.
    """
    list_display = ['nombre', 'fecha_inicio', 'fecha_fin']


@admin.register(PeriodoPPDA)
class PeriodoPPDAAdmin(admin.ModelAdmin):
    """Admin para el modelo PeriodoPPDA con validación de fechas."""
    list_display = ['ppda', 'anio', 'inicio_periodo', 'fin_periodo']

    def save_model(self, request, obj, form, change):
        """
        Valida que la fecha de inicio sea anterior a la fecha de fin.
        """
        if obj.inicio_periodo > obj.fin_periodo:
            from django.contrib import messages
            messages.error(
                request, "La fecha de inicio no puede ser posterior a la fecha de fin.")
            logger = logging.getLogger(__name__)
            logger.error(
                f"PeriodoPPDA inválido por {request.user}: {obj.inicio_periodo} > {obj.fin_periodo}")
            return

        super().save_model(request, obj, form, change)
