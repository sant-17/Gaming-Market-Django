from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path('', views.index, name = 'index'),

    path('loginFormulario/', views.loginFormulario, name = 'loginFormulario'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('tienda/', views.tienda, name = 'tienda'),

    # PROVEEDORES
    path('proveedores/', views.listarProveedores, name="listarProveedores"),
    path('formularioProveedor/', views.formularioProveedor, name="formularioProveedor"),
    path('guardarProveedor/', views.guardarProveedor, name="guardarProveedor"),
    path('deshabilitarProveedor/<id>', views.deshabilitarProveedor, name="deshabilitarProveedor"),
    path('habilitarProveedor/<id>', views.habilitarProveedor, name="habilitarProveedor"),
    path('edicionProveedor/<id>', views.edicionProveedor, name="edicionProveedor"),
    path('editarProveedor/', views.editarProveedor, name="editarProveedor"),
    path('buscarProveedor/', views.buscarProveedor, name="buscarProveedor"),
    
    # GENEROS
    path('generos/', views.listarGeneros, name="listarGeneros"),
    path('formularioGenero/', views.formularioGenero, name="formularioGenero"),
    path('guardarGenero/', views.guardarGenero, name="guardarGenero"),
    path('eliminarGenero/<id>', views.eliminarGenero, name="eliminarGenero"),
    path('edicionGenero/<id>', views.edicionGenero, name="edicionGenero"),
    path('editarGenero/', views.editarGenero, name="editarGenero"),
    
    # JUEGOS
    path('juegos/', views.listarJuegos, name="listarJuegos"),
    path('formularioJuego/', views.formularioJuego, name="formularioJuego"),
    path('guardarJuego/', views.guardarJuego, name="guardarJuego"),
    path('eliminarJuego/<id>', views.eliminarJuego, name="eliminarJuego"),
    path('edicionJuego/<id>', views.edicionJuego, name="edicionJuego"),
    path('editarJuego/', views.editarJuego, name="editarJuego"),
    path('buscarJuego/', views.buscarJuego, name="buscarJuego"),

    # EMPLEADOS
    path('empleados/', views.listarUsuariosEmpleados, name="listarEmpleados"),
    path('formularioEmpleado/', views.formularioUsuarioEmpleado, name="formularioUsuarioEmpleado"),
    path('guardarEmpleado/', views.guardarUsuarioEmpleado, name="guardarUsuarioEmpleado"),
    path('deshabilitarEmpleado/<id>', views.deshabilitarUsuarioEmpleado, name="deshabilitarEmpleado"),
    path('habilitarEmpleado/<id>', views.habilitarUsuarioEmpleado, name="habilitarEmpleado"),
    path('edicionEmpleado/<id>', views.edicionUsuarioEmpleado, name="edicionUsuarioEmpleado"),
    path('editarEmpleado/', views.editarUsuarioEmpleado, name="editarUsuarioEmpleado"),
    path('buscarEmpleado/', views.buscarEmpleado, name="buscarEmpleado"),
]