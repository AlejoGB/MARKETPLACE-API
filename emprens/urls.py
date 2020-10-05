from django.urls import path
from .views import EmprendimientoListView, EmprendimientoBarrioView, EmprendimientoDetailView, EmprendimientoCreateView, EmprendimientoRUDView, ProductoListView, ProductoCreateView, ProductoRUDView

app_name = 'emprens'

urlpatterns = [
    path('', EmprendimientoListView.as_view(), name='empren-list'),
    path('barrio/<barrio>/', EmprendimientoBarrioView.as_view(), name='barrio-list'),
    path('detail/<pk>/', EmprendimientoDetailView.as_view(), name='empren-detail'),
    path('<pk>/productos/', ProductoListView.as_view(), name='empren-productos'),

    #CRUD EMPRENDIMIENTOS
    path('create/', EmprendimientoCreateView.as_view(), name='empren-create'),
    path('<pk>/rud/', EmprendimientoRUDView.as_view(), name='empren-rud'),

    #CRUD PRODUCTOS
    path('<pk>/producto/create/', ProductoCreateView.as_view(), name='producto-create'),
    path('producto/rud/<pk>/', ProductoRUDView.as_view(), name='producto-rud'),
]