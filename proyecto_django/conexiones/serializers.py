import logging
from rest_framework import serializers
from .models import (
    Organismo, Medida, PPDA, PeriodoPPDA, Indicador,
    Reporte, Cumplimiento, AsignacionIndicador, UsuarioPerfil
)

logger = logging.getLogger(__name__)


class OrganismoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Organismo.
    """
    class Meta:
        model = Organismo
        fields = ['id', 'nombre', 'region']


class IndicadorSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Indicador.
    """
    class Meta:
        model = Indicador
        fields = ['id', 'descripcion', 'formula_calculo', 'medio_verificacion']


class PPDACompactSerializer(serializers.ModelSerializer):
    """
    Serializer compacto para representar un PPDA solo con nombre e ID.
    """
    class Meta:
        model = PPDA
        fields = ['id', 'nombre']


class PeriodoPPDASerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PeriodoPPDA.
    """
    ppda = PPDACompactSerializer(read_only=True)

    class Meta:
        model = PeriodoPPDA
        fields = ['id', 'ppda', 'anio', 'inicio_periodo', 'fin_periodo']


class MedidaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Medida.
    Incluye validaciones de lógica de negocio.
    """
    organismo = OrganismoSerializer(read_only=True)
    indicador = IndicadorSerializer(read_only=True)
    ppda = PPDACompactSerializer(read_only=True)
    periodo_ppda = PeriodoPPDASerializer(read_only=True)

    class Meta:
        model = Medida
        fields = [
            'id',
            'organismo',
            'referencia_pda',
            'tipo_medida',
            'nombre_corto',
            'indicador',
            'frecuencia',
            'regulatoria',
            'ppda',
            'periodo_ppda',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):
        """
        Validación de reglas de negocio para medidas.
        """
        try:
            if data.get('regulatoria') and not data.get('frecuencia'):
                logger.warning(
                    "Validación fallida: medida regulatoria sin frecuencia")
                raise serializers.ValidationError(
                    "Debe especificar la frecuencia si la medida es regulatoria.")

            if data.get('tipo_medida') and not data.get('regulatoria'):
                logger.warning(
                    "Validación fallida: tipo de medida definido sin campo regulatoria")
                raise serializers.ValidationError(
                    "No se puede definir tipo de medida sin indicar si es regulatoria o no.")

            return data
        except Exception as e:
            logger.error(f"Error de validación en MedidaSerializer: {e}")
            raise


class ReporteSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Reporte, incluye relaciones anidadas.
    """
    organismo = OrganismoSerializer(read_only=True)
    medida = MedidaSerializer(read_only=True)

    class Meta:
        model = Reporte
        fields = [
            'id',
            'fecha',
            'año_calendario',
            'estado',
            'organismo',
            'medida',
            'created_at',
            'updated_at',
        ]


class CumplimientoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Cumplimiento.
    """
    medida = MedidaSerializer(read_only=True)

    class Meta:
        model = Cumplimiento
        fields = [
            'id',
            'medida',
            'porcentaje_cumplimiento',
            'created_at',
            'updated_at',
        ]


class AsignacionIndicadorSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo AsignacionIndicador.
    """
    organismo = OrganismoSerializer(read_only=True)
    indicador = IndicadorSerializer(read_only=True)

    class Meta:
        model = AsignacionIndicador
        fields = [
            'id',
            'organismo',
            'indicador',
            'fecha_asignacion',
            'observaciones',
            'activo'
        ]


class UsuarioPerfilSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UsuarioPerfil.
    """
    user = serializers.StringRelatedField()
    organismo_asociado = OrganismoSerializer(read_only=True)

    class Meta:
        model = UsuarioPerfil
        fields = [
            'id',
            'user',
            'rol',
            'organismo_asociado'
        ]
