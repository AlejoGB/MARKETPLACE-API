from django.urls import path
from .views import EmprendimientoListView, EmprendimientoBarrioView, EmprendimientoDetailView, EmprendimientoCreateView, ProductoListView, ProductoCreateView

app_name = 'emprens'

urlpatterns = [
    path('', EmprendimientoListView.as_view(), name='empren-list'),
    path('barrio/<barrio>/', EmprendimientoBarrioView.as_view(), name='barrio-list'),
    path('detail/<pk>/', EmprendimientoDetailView.as_view(), name='empren-detail'),
    path('<pk>/productos', ProductoListView.as_view(), name='empren-productos'),

    #CRUD EMPRENDIMIENTOS
    path('create/', EmprendimientoCreateView.as_view(), name='empren-create'),

    #CRUD PRODUCTOS
    path('<pk>/producto/create', ProductoCreateView.as_view(), name='producto-create')
]