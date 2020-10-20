from core.models import Emprendimiento, Producto
from rest_framework import serializers





class EmprendimientoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Emprendimiento
        fields = [
            'pk',
            'name',
            'tag',
            'subtag',
            'slug',
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
            'owner'
        ]
        #extra_kwargs = {
        #    'owner': {'required': True}
        #}
        #read_only_fields = ['pk', 'owner']
    
    def create(self, validated_data):
        return Emprendimiento.objects.create(**validated_data)



class ProductoSerializer(serializers.ModelSerializer):
    emprendimiento = serializers.ReadOnlyField(source='emprendimiento.name')
    class Meta:
        model = Producto
        fields = [
            'pk',
            'name',
            'tag',
            'descripcion',
            'imagen',
            'precio',
            'inmediato',
            'stock',
            'emprendimiento'
        ]
        # depth = 1
        read_only_fields = ['pk']

    def create(self, validated_data):
        return Producto.objects.create(**validated_data)