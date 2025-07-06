from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inicio/', views.inicio),
    path('productos/', views.vista_productos, name='productos'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('confirmar/', views.confirmar_carrito, name='confirmar_carrito'),
]
