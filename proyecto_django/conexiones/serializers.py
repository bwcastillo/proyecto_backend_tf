from rest_framework import serializers
from .models import Organismo, Medida


class OrganismoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organismo
        fields = ['id_organismo', 'nombre',  'region']


class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = [
            'id_medida',
            'id_organismo',
            'referencia_pda',
            'tipo_medida',
            'nombre_corto',
            'indicador',
            'formula',
            'frecuencia',
            'verificacion',
            'regulatoria',
        ]
