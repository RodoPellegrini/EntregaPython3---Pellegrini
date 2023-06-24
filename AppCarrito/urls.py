from django.urls import path
from AppCarrito import views



urlpatterns = [
    path('', views.inicio, name='inicio' ),
    #path('probando_template/', views.probando_template, name='probando_template'),
    path('mostrar_carrito/', views.mostrar_carrito, name='mostrar_carrito'),
    path('busqueda_producto/', views.busqueda_productos, name='busqueda_producto'),
    path('procesar_pedidos/', views.procesar_pedidos, name='procesar_pedidos'),  
]