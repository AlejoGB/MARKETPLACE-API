from .serializers import EmprendimientoSerializer, ProductoSerializer
from rest_framework import generics, permissions, status
from core.models import Emprendimiento, Producto
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
# from django.shortcuts import render

# Create your views here.


class EmprendimientoListView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = EmprendimientoSerializer

    def get_queryset(self):
        return Emprendimiento.objects.all().order_by('-id')


class EmprendimientoBarrioView(generics.ListAPIView):
    
    serializer_class = EmprendimientoSerializer
    
    def get_queryset(self):
        barrio = self.kwargs['barrio']
        return Emprendimiento.objects.filter(barrio__iexact=barrio)


class EmprendimientoDetailView(generics.RetrieveAPIView):
    permission_classes = (IsOwnerOrReadOnly, )
    # Vista de detaille    
    serializer_class = EmprendimientoSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Emprendimiento.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class EmprendimientoCreateView(generics.CreateAPIView):
    # Create VIEW
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = EmprendimientoSerializer

    def post(self, request):
        serializer = EmprendimientoSerializer(data=request.data)


        user_db = User.objects.get(email=user.email)
        if user_db.is_owner == False:
            if serializer.is_valid():
                serializer.save(owner=request.user)
                user_db.is_owner = True
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoListView(generics.ListAPIView):
    serializer_class = ProductoSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    def get_queryset(self):
        emprendimiento = self.kwargs['pk']
        productos = Producto.objects.filter(emprendimiento=emprendimiento)
        return productos

