
from django.shortcuts import render, redirect
from .models import *

# Mensajes tipo cookies temporales
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'webapp/index.html')

def listarProveedores(request):
    return render(request, 'webapp/proveedor/listar_proveedores.html', {'proveedores': Proveedor.objects.all()})

def formularioProveedor(request):
    return render(request, 'webapp/proveedor/formulario_proveedor.html')

def guardarProveedor(request):
    try:
        if request.method == "POST":
            proveedor = Proveedor(
                nombre=request.POST['nombre'],
                email=request.POST['email'],
                telefono=request.POST['telefono'],
            )
            proveedor.save()
            messages.success(request, "Proveedor guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioProveedor')

def listarGeneros(request):
    return render(request, 'webapp/genero/listar_generos.html', {'generos': Genero.objects.all()})

def eliminarGenero(request, id):
    genero = Genero.objects.get(id = id)
    genero.delete()
    return redirect('webapp:listarGeneros')

def edicionGenero(request, id):
    genero = Genero.objects.get(id = id)
    return render(request, 'webapp/genero/edicion_genero.html', {'genero': genero})

def editarGenero(request):
    try:
        if request.method == "POST":
            genero = Genero(
                id = request.POST['id'],
                nombre=request.POST['nombre'],
            )
            genero.save()
            messages.success(request, "Genero editado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarGeneros')

def formularioGenero(request):
    return render(request, 'webapp/genero/formulario_genero.html')

def guardarGenero(request):
    try:
        if request.method == "POST":
            genero = Genero(
                nombre=request.POST['nombre'],
            )
            genero.save()
            messages.success(request, "Genero guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioGenero')

def listarJuegos(request):
    return render(request, 'webapp/juego/listar_juegos.html', {'juegos': Juego.objects.all()})

def formularioJuego(request):
    return render(request, 'webapp/juego/formulario_juego.html', {"generos": Genero.objects.all()})

def guardarJuego(request):
    try:
        if request.method == "POST":
            juego = Juego(
                titulo = request.POST['titulo'],
                fecha_lanzamiento = request.POST['fecha_lanzamiento'],
                desarrollador = request.POST['desarrollador'],
                editor = request.POST['editor'],
                descripcion = request.POST['descripcion'],
                esrb = request.POST['esrb'],
                multijugador = request.POST['multijugador'],
                stock = request.POST['stock'],
                precio = request.POST['precio'],
                imagen = request.POST['imagen'],
                habilitado = request.POST['habilitado']
            )
            juego.save()
            generos = request.POST.getlist('generos')
            for generoID in generos:
                genero = Genero.objects.get(id=int(generoID))
                juego.generos.add(genero)
            juego.save()
            messages.success(request, "Juego guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioJuego')

def listarCompras(request):
    return render(request, 'webapp/compra/listar_compras.html', {'compras': Compra.objects.all()})

def formularioCompra(request):
    return render(request, 'webapp/compra/formulario_compra.html', {"proveedores": Proveedor.objects.all()})

def guardarCompra(request):
    try:
        if request.method == "POST":
            proveedorID = request.POST['proveedor']
            proveedor = Proveedor.objects.get(id=int(proveedorID))

            compra = Compra(
                fecha = request.POST['fecha'],
                valor = request.POST['valor'],
                id_proveedor = proveedor
            )
            compra.save()
            messages.success(request, "Compra guardada correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioCompra')

def listarPermisos(request):
    return render(request, 'webapp/permiso/listar_permisos.html', {'permisos': Permiso.objects.all()})

def formularioPermiso(request):
    return render(request, 'webapp/permiso/formulario_permiso.html')

def guardarPermiso(request):
    try:
        if request.method == "POST":
            permiso = Permiso(
                nombre=request.POST['nombre'],
            )
            permiso.save()
            messages.success(request, "Permiso guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioPermiso')

def listarRoles(request):
    return render(request, 'webapp/rol/listar_roles.html', {'roles': Rol.objects.all()})

def formularioRol(request):
    return render(request, 'webapp/rol/formulario_rol.html', {"permisos": Permiso.objects.all()})

def guardarRol(request):
    try:
        if request.method == "POST":
            rol = Rol(
                nombre = request.POST['nombre'],
            )
            rol.save()
            permisos = request.POST.getlist('permisos')
            for permisoID in permisos:
                permiso = Permiso.objects.get(id=int(permisoID))
                rol.permisos.add(permiso)
            rol.save()
            messages.success(request, "Rol guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioRol')

def listarUsuarios(request):
    return render(request, 'webapp/usuario/listar_usuarios.html', {'usuarios': Usuario.objects.all()})

def formularioUsuario(request):
    return render(request, 'webapp/usuario/formulario_usuario.html', {"roles": Rol.objects.all()})

def guardarUsuario(request):
    try:
        if request.method == "POST":
            rolID = request.POST['rol']
            rol = Rol.objects.get(id=int(rolID))

            usuario = Usuario(
                email = request.POST['email'],
                clave = request.POST['clave'],
                id_rol = rol,
            )
            usuario.save()
            messages.success(request, "Usuario guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioUsuario')

def listarEmpleados(request):
    return render(request, 'webapp/empleado/listar_empleados.html', {'empleados': Empleado.objects.all()})

def formularioEmpleado(request):
    return render(request, 'webapp/empleado/formulario_empleado.html', {"usuarios": Usuario.objects.all()})

def guardarEmpleado(request):
    try:
        if request.method == "POST":
            usuarioID = request.POST['usuario']
            usuario = Usuario.objects.get(id=int(usuarioID))

            empleado = Empleado(
                cedula = request.POST['cedula'],
                nombre = request.POST['nombre'],
                apellido = request.POST['apellido'],
                telefono = request.POST['telefono'],
                fecha_nacimiento = request.POST['fecha_nacimiento'],
                municipio_residencia = request.POST['municipio_residencia'],
                direccion_residencia = request.POST['direccion_residencia'],
                id_usuario = usuario,
            )
            empleado.save()
            messages.success(request, "Empleado guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioEmpleado')

def listarClientes(request):
    return render(request, 'webapp/cliente/listar_clientes.html', {'clientes': Cliente.objects.all()})

def formularioCliente(request):
    return render(request, 'webapp/cliente/formulario_cliente.html', {"usuarios": Usuario.objects.all()})

def guardarCliente(request):
    try:
        if request.method == "POST":
            usuarioID = request.POST['usuario']
            usuario = Usuario.objects.get(id=int(usuarioID))

            cliente = Cliente(
                nombre = request.POST['nombre'],
                apellido = request.POST['apellido'],
                fecha_nacimiento = request.POST['fecha_nacimiento'],
                id_usuario = usuario,
            )
            cliente.save()
            messages.success(request, "Cliente guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioCliente')

def listarVentas(request):
    return render(request, 'webapp/venta/listar_ventas.html', {'ventas': Venta.objects.all()})

def formularioVenta(request):
    return render(request, 'webapp/venta/formulario_venta.html', {"clientes": Cliente.objects.all()})

def guardarVenta(request):
    try:
        if request.method == "POST":
            clienteID = request.POST['cliente']
            cliente = Cliente.objects.get(id=int(clienteID))

            venta = Venta(
                total = request.POST['total'],
                id_cliente = cliente
            )
            venta.save()
            messages.success(request, "Venta guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioVenta')