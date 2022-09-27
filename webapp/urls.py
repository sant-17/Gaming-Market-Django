from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path('', views.index, name = 'index'),

    path('listarProveedores/', views.listarProveedores, name="listarProveedores"),
    path('edicionProveedor/<id>', views.edicionProveedor, name="edicionProveedor"),
    path('edicitaProveedor/', views.editarProveedor, name="editarProveedor"),
    path('eliminarProveedor/<id>', views.eliminarProveedor, name="eliminarProveedor"),
    path('formularioProveedor/', views.formularioProveedor, name="formularioProveedor"),
    path('guardarProveedor/', views.guardarProveedor, name="guardarProveedor"),

    path('listarGeneros/', views.listarGeneros, name="listarGeneros"),
    path('edicionGenero/<id>', views.edicionGenero, name="edicionGenero"),
    path('edicitarGenero/', views.editarGenero, name="editarGenero"),
    path('eliminarGenero/<id>', views.eliminarGenero, name="eliminarGenero"),
    path('formularioGenero/', views.formularioGenero, name="formularioGenero"),
    path('guardarGenero/', views.guardarGenero, name="guardarGenero"),

    path('listarJuegos/', views.listarJuegos, name="listarJuegos"),
    path('edicionJuego/<id>', views.edicionJuego, name="edicionJuego"),
    path('edicitaJuego/', views.editarJuego, name="editarJuego"),
    path('eliminarJuego/<id>', views.eliminarJuego, name="eliminarJuego"),
    path('formularioJuego/', views.formularioJuego, name="formularioJuego"),
    path('guardarJuego/', views.guardarJuego, name="guardarJuego"),

    path('listarCompras/', views.listarCompras, name="listarCompras"),
    path('formularioCompra/', views.formularioCompra, name="formularioCompra"),
    path('guardarCompra/', views.guardarCompra, name="guardarCompra"),

    path('listarPermisos/', views.listarPermisos, name="listarPermisos"),
    path('edicionPermiso/<id>', views.edicionPermiso, name="edicionPermiso"),
    path('edicitaPermiso/', views.editarPermiso, name="editarPermiso"),
    path('eliminarPermiso/<id>', views.eliminarPermiso, name="eliminarPermiso"),
    path('formularioPermiso/', views.formularioPermiso, name="formularioPermiso"),
    path('guardarPermiso/', views.guardarPermiso, name="guardarPermiso"),

    path('listarRoles/', views.listarRoles, name="listarRoles"),
    path('formularioRol/', views.formularioRol, name="formularioRol"),
    path('guardarRol/', views.guardarRol, name="guardarRol"),

    path('listarUsuarios/', views.listarUsuarios, name="listarUsuarios"),
    path('formularioUsuario/', views.formularioUsuario, name="formularioUsuario"),
    path('guardarUsuario/', views.guardarUsuario, name="guardarUsuario"),

    path('listarEmpleados/', views.listarEmpleados, name="listarEmpleados"),
    path('formularioEmpleado/', views.formularioEmpleado, name="formularioEmpleado"),
    path('guardarEmpleado/', views.guardarEmpleado, name="guardarEmpleado"),

    path('listarClientes/', views.listarClientes, name="listarClientes"),
    path('formularioCliente/', views.formularioCliente, name="formularioCliente"),
    path('guardarCliente/', views.guardarCliente, name="guardarCliente"),

    path('listarVentas/', views.listarVentas, name="listarVentas"),
    path('formularioVenta/', views.formularioVenta, name="formularioVenta"),
    path('guardarVenta/', views.guardarVenta, name="guardarVenta"),
]