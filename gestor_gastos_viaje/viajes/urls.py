# viajes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('gastos/registrar/', views.registrar_gasto_view, name='registrar_gasto'),
    path('viajes/registrar/', views.registrar_viaje, name='registrar_viaje'),
    path('viajes/lista/', views.lista_viajes_con_gastos, name='lista_viajes'),


]
