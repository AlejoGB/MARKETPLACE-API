from core.models import Emprendimiento
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