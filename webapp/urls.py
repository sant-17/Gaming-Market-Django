from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path('', views.index, name = 'index'),

    # PROVEEDORES
    path('proveedores/', views.listarProveedores, name="listarProveedores"),
    path('formularioProveedor/', views.formularioProveedor, name="formularioProveedor"),
    path('guardarProveedor/', views.guardarProveedor, name="guardarProveedor"),
    path('deshabilitarProveedor/<id>', views.deshabilitarProveedor, name="deshabilitarProveedor"),
    path('habilitarProveedor/<id>', views.habilitarProveedor, name="habilitarProveedor"),
    path('edicionProveedor/<id>', views.edicionProveedor, name="edicionProveedor"),
    path('editarProveedor/', views.editarProveedor, name="editarProveedor"),
    path('proveedoresDeshabilitados/', views.listarProveedoresDeshabilitados, name="listarProveedoresDeshabilitados"),
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
    
    # COMPRAS
    path('compras/', views.listarCompras, name="listarCompras"),
    path('formularioCompra/', views.formularioCompra, name="formularioCompra"),
    path('guardarCompra/', views.guardarCompra, name="guardarCompra"),

    # EMPLEADOS
    path('empleados/', views.listarUsuariosEmpleados, name="listarEmpleados"),
    path('formularioEmpleado/', views.formularioUsuarioEmpleado, name="formularioUsuarioEmpleado"),
    path('guardarEmpleado/', views.guardarUsuarioEmpleado, name="guardarUsuarioEmpleado"),
    path('deshabilitarEmpleado/<id>', views.deshabilitarUsuarioEmpleado, name="deshabilitarUsuarioEmpleado"),
    path('habilitarEmpleado/<id>', views.habilitarUsuarioEmpleado, name="habilitarUsuarioEmpleado"),
    path('edicionEmpleado/<id>', views.edicionUsuarioEmpleado, name="edicionUsuarioEmpleado"),
    path('editarEmpleado/', views.editarUsuarioEmpleado, name="editarUsuarioEmpleado"),
    path('empleadosDeshabilitados/', views.listarUsuariosEmpleadosDeshabilitados, name="listarEmpleadosDeshabilitados"),
    
    # VENTAS
    path('ventas/', views.listarVentas, name="listarVentas"),
    path('formularioVenta/', views.formularioVenta, name="formularioVenta"),
    path('guardarVenta/', views.guardarVenta, name="guardarVenta"),
]