from django.urls import path
from .views import EmprendimientoListView, EmprendimientoBarrioView, EmprendimientoCRUDView, ProductoListView

app_name = 'emprens'

urlpatterns = [
    path('', EmprendimientoListView.as_view(), name='empren-list'),
    path('barrio/<barrio>/', EmprendimientoBarrioView.as_view(), name='barrio-list'),
    path('<pk>/', EmprendimientoCRUDView.as_view(), name='empren-crud'),
    path('<pk>/productos', ProductoListView.as_view(), name='empren-productos'),
]