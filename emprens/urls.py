from django.urls import path
from .views import EmprendimientoListView, EmprendimientoBarrioView, EmprendimientoCRUDView

app_name = 'emprens'

urlpatterns = [
    path('', EmprendimientoListView.as_view(), name='empren-list'),
    path('<barrio>/', EmprendimientoBarrioView.as_view(), name='barrio-list'),
    path('id/<pk>/', EmprendimientoCRUDView.as_view(), name='empren-crud')
]