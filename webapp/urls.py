from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [

    # TIENDA
    path('', views.index, name = 'index'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('sign-up/', views.signup, name = 'signup'),
    path('save/', views.guardarCliente, name = 'save'),
    
    path('vaciar/', views.vaciarCarrito, name = 'vaciar'),
    path('shop/', views.tienda, name = 'tienda'),
    path('product/<id>', views.producto, name = 'producto'),
    path('cart/', views.verCarrito, name = 'verCarrito'),
    path('agregarAlCarrito/<id>', views.agregarAlCarrito, name="agregarAlCarrito"),
    path('aumentarEnCarrito/<id>', views.aumentarEnCarrito, name="aumentarEnCarrito"),
    path('restar/<int:id>', views.restarJuego, name="restarJuego"),
    path('eliminarJuegoCarrito/<id>', views.eliminarJuegoDelCarrito, name="eliminarJuegoCar"),
    path('cheackout/', views.checkout, name = 'checkout'),
    path('venta/', views.venta, name = 'venta'),

    # INICIO DE SESIÓN CRUD
    path('login-empleados/', views.formLoginCrud, name = 'loginEmpleados'),
    path('login-crud/', views.loginCrud, name = 'loginCrud'),
    path('logout-crud/', views.logoutCrud, name = 'logoutCrud'),
    path('inicio-crud/', views.inicioCrud, name = 'inicioCrud'),

    # PROVEEDORES
    path('proveedores/', views.listarProveedores, name="listarProveedores"),
    path('proveedores/nuevo', views.formularioProveedor, name="formularioProveedor"),
    path('guardarProveedor/', views.guardarProveedor, name="guardarProveedor"),
    path('deshabilitarProveedor/<id>', views.deshabilitarProveedor, name="deshabilitarProveedor"),
    path('habilitarProveedor/<id>', views.habilitarProveedor, name="habilitarProveedor"),
    path('proveedores/actualizar-proveedor/<id>', views.edicionProveedor, name="edicionProveedor"),
    path('editarProveedor/', views.editarProveedor, name="editarProveedor"),
    path('buscarProveedor/', views.buscarProveedor, name="buscarProveedor"),
    
    # GENEROS
    path('generos/', views.listarGeneros, name="listarGeneros"),
    path('generos/nuevo', views.formularioGenero, name="formularioGenero"),
    path('guardarGenero/', views.guardarGenero, name="guardarGenero"),
    path('eliminarGenero/<id>', views.eliminarGenero, name="eliminarGenero"),
    path('edicionGenero/<id>', views.edicionGenero, name="edicionGenero"),
    path('editarGenero/', views.editarGenero, name="editarGenero"),
    
    # JUEGOS
    path('juegos/', views.listarJuegos, name="listarJuegos"),
    path('juegos/nuevo', views.formularioJuego, name="formularioJuego"),
    path('guardarJuego/', views.guardarJuego, name="guardarJuego"),
    path('eliminarJuego/<id>', views.eliminarJuego, name="eliminarJuego"),
    path('juegos/actualizar/<id>', views.edicionJuego, name="edicionJuego"),
    path('editarJuego/', views.editarJuego, name="editarJuego"),
    path('buscarJuego/', views.buscarJuego, name="buscarJuego"),

    # EMPLEADOS
    path('empleados/', views.listarUsuariosEmpleados, name="listarEmpleados"),
    path('empleados/nuevo', views.formularioUsuarioEmpleado, name="formularioUsuarioEmpleado"),
    path('guardarEmpleado/', views.guardarUsuarioEmpleado, name="guardarUsuarioEmpleado"),
    path('deshabilitarEmpleado/<id>', views.deshabilitarUsuarioEmpleado, name="deshabilitarEmpleado"),
    path('habilitarEmpleado/<id>', views.habilitarUsuarioEmpleado, name="habilitarEmpleado"),
    path('empleados/actualizar/<id>', views.edicionUsuarioEmpleado, name="edicionUsuarioEmpleado"),
    path('editarEmpleado/', views.editarUsuarioEmpleado, name="editarUsuarioEmpleado"),
    path('buscarEmpleado/', views.buscarEmpleado, name="buscarEmpleado"),
    
    #CLIENTES
    path('editarCliente/', views.editarUsuarioCliente, name="editarUsuarioCliente"),
    path('perfilcliente/', views.miPerfil, name="perfilCliente"),
]