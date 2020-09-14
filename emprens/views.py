from .serializers import EmprendimientoSerializer
from rest_framework import generics
from core.models import Emprendimiento
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


class EmprendimientoCRUDView(generics.RetrieveAPIView): 
    # por ahora solo RETRIEVE    # Detailview , CreateView , FormView
    # una vez implementados los usuarios: CREATE UPDATE DELETE                        
    serializer_class = EmprendimientoSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Emprendimiento.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

