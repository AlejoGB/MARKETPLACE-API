from core.models import Emprendimiento, Producto
from rest_framework import serializers


class EmprendimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Emprendimiento
        fields = [
            'pk',
            'name',
            'tag',
            'subtag',
            'descripcion',
            'logo',
            'cont_mail',
            'cont_insta',
            'cont_whatsapp',
            'direccion',
            'barrio',
            'ciudad',
            'cobertura',
            'horario',
            'envio',
        ]

        read_only_fields = ['pk']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'emprendimiento',
            'pk',
            'name',
            'tag',
            'descripcion',
            'imagen',
            'precio',
            'inmediato',
            'stock'
        ]
        # depth = 1
        read_only_fields = ['pk']