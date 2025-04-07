from rest_framework import serializers
from .models import Organismo, Medida


class OrganismoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organismo
        fields = ['id_organismo', 'nombre', 'region']


class MedidaSerializer(serializers.ModelSerializer):
    organismo = OrganismoSerializer(read_only=True)
    indicador = serializers.StringRelatedField(read_only=True)  # o un IndicadorSerializer

    class Meta:
        model = Medida
        fields = [
            'id_medida',
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
