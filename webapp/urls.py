from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path('', views.index, name = 'index'),

    path('formularioProveedor/', views.formularioProveedor, name="formularioProveedor"),
    path('guardarProveedor/', views.guardarProveedor, name="guardarProveedor"),

    path('formularioGenero/', views.formularioGenero, name="formularioGenero"),
    path('guardarGenero/', views.guardarGenero, name="guardarGenero"),

    path('formularioJuego/', views.formularioJuego, name="formularioJuego"),
    path('guardarJuego/', views.guardarJuego, name="guardarJuego"),

    path('formularioCompra/', views.formularioCompra, name="formularioCompra"),
    path('guardarCompra/', views.guardarCompra, name="guardarCompra"),

    path('formularioPermiso/', views.formularioPermiso, name="formularioPermiso"),
    path('guardarPermiso/', views.guardarPermiso, name="guardarPermiso"),

    path('formularioRol/', views.formularioRol, name="formularioRol"),
    path('guardarRol/', views.guardarRol, name="guardarRol"),

    path('formularioUsuario/', views.formularioUsuario, name="formularioUsuario"),
    path('guardarUsuario/', views.guardarUsuario, name="guardarUsuario"),

    path('formularioEmpleado/', views.formularioEmpleado, name="formularioEmpleado"),
    path('guardarEmpleado/', views.guardarEmpleado, name="guardarEmpleado"),

    path('formularioCliente/', views.formularioCliente, name="formularioCliente"),
    path('guardarCliente/', views.guardarCliente, name="guardarCliente"),

    path('formularioVenta/', views.formularioVenta, name="formularioVenta"),
    path('guardarVenta/', views.guardarVenta, name="guardarVenta"),
]