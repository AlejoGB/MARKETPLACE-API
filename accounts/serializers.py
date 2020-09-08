from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        # crea un usuario con pw encriptada y la devuelve
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    # serializer for user auth object
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        # valida y autentifica al usuario
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Credenciales invalidas, no se puede autentificar')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs