from .serializers import EmprendimientoSerializer, ProductoSerializer
from rest_framework import generics, permissions, status
from core.models import Emprendimiento, Producto, User
from .permissions import IsOwnerOrReadOnly, IsParentOwnerOrReadOnly
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
    permission_classes = (permissions.IsAuthenticated, )
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
        user_db = User.objects.get(email=request.user.email)
        # un emprendimiento por usuario
        if user_db.is_owner == False:
            if serializer.is_valid():
                serializer.save(owner=request.user)
                user_db.is_owner = True
                user_db.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        if serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('aaa')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoListView(generics.ListAPIView):
    serializer_class = ProductoSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    def get_queryset(self):
        emprendimiento = self.kwargs['pk']
        productos = Producto.objects.filter(emprendimiento=emprendimiento)
        return productos


class ProductoCreateView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenticated, IsParentOwnerOrReadOnly, )
    serializer_class = ProductoSerializer

    def post(self, request, **kwargs):    
        serializer = ProductoSerializer(data=request.data)
        user_db = User.objects.get(email=request.user.email)
        empren = Emprendimiento.objects.getByOwner(owner=user_db)
        if empren is None:
            return Response('El usuario no posee emprendimientos asociados a su nombre', status=status.HTTP_403_FORBIDDEN)
        # un emprendimiento por usuario
        if user_db.is_owner == True and int(self.kwargs['pk']) == int(empren.pk):
            print('debug: valid auth and permision')
            if serializer.is_valid():
                serializer.save(emprendimiento=empren)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        if serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        else:
            print(serializer.data)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


