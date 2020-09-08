from accounts.serializers import UserSerializer, AuthTokenSerializer
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    # Crea un usuario nuevo
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    # crea un token de autentificacion para el usuario
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

