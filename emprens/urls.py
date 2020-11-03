from django.urls import path
from .views import EmprendimientoListView, EmprendimientoBarrioView, EmprendimientoOwnerView, EmprendimientoDetailView, EmprendimientoCreateView, EmprendimientoRUDView, ProductoListView, ProductoCreateView, ProductoRUDView

app_name = 'emprens'

urlpatterns = [
    path('', EmprendimientoListView.as_view(), name='empren-list'),
    path('barrio/<barrio>/', EmprendimientoBarrioView.as_view(), name='barrio-list'),
    path('detail/<slug>/', EmprendimientoDetailView.as_view(), name='empren-detail'),
    path('<slug>/productos/', ProductoListView.as_view(), name='empren-productos'),
    path('owner/<owner>/', EmprendimientoOwnerView.as_view(), name='empren-owner'),
    #CRUD EMPRENDIMIENTOS
    path('create/', EmprendimientoCreateView.as_view(), name='empren-create'),
    path('<slug>/rud/', EmprendimientoRUDView.as_view(), name='empren-rud'),

    #CRUD PRODUCTOS
    path('<slug>/producto/create/', ProductoCreateView.as_view(), name='producto-create'),
    path('producto/rud/<pk>/', ProductoRUDView.as_view(), name='producto-rud'),
]