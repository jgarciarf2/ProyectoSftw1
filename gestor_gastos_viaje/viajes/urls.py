# viajes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('gastos/agregar/', views.registrar_gasto, name='registrar_gasto'),
    path('viajes/agregar/', views.registrar_viaje, name='registrar_viaje'),
    path('viajes/', views.lista_viajes, name='lista_viajes'),
    path('viajes/<int:viaje_id>/', views.detalle_viaje, name='detalle_viaje'),
    path('gastos/agregar/<int:viaje_id>/', views.registrar_gasto, name='registrar_gasto'),
]
