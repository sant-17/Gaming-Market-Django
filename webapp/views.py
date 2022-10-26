
from django.shortcuts import render, redirect
from .models import *

# Mensajes tipo cookies temporales
from django.contrib import messages

# Gestión de errores de base de datos
from django.db import IntegrityError    

# Create your views here.

def index(request):
    return render(request, 'webapp/index.html')



# PROVEEDORES
def listarProveedores(request):
    proveedores = Proveedor.objects.filter(habilitado = True)
    return render(request, 'webapp/proveedor/listar_proveedores.html', {'proveedores': proveedores})

def listarProveedoresDeshabilitados(request):
    proveedores = Proveedor.objects.filter(habilitado = False)
    return render(request, 'webapp/proveedor/listar_proveedores.html', {'proveedores': proveedores})

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
            messages.success(request, f"Proveedor ({proveedor.nombre}) creado exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')

def deshabilitarProveedor(request, id):
    try:
        proveedor = Proveedor.objects.get(id = id)
        proveedor.habilitado = False
        proveedor.save()
        messages.success(request, f"Proveedor ({proveedor.nombre}) deshabilitado exitosamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')

def habilitarProveedor(request, id):
    try:
        proveedor = Proveedor.objects.get(id = id)
        proveedor.habilitado = True
        proveedor.save()
        messages.success(request, f"Proveedor ({proveedor.nombre}) habilitado exitosamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')

def edicionProveedor(request, id):
    proveedor = Proveedor.objects.get(id = id)
    return render(request, 'webapp/proveedor/edicion_proveedor.html', {'proveedor': proveedor})

def editarProveedor(request):
    try:
        if request.method == "POST":
            proveedor = Proveedor.objects.get(id = request.POST['id'])
            proveedor.nombre = request.POST['nombre']
            proveedor.email = request.POST['email']
            proveedor.telefono = request.POST['telefono']
            proveedor.save()
            messages.success(request, f"Proveedor ({proveedor.nombre}) editado exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')



# GENEROS
def listarGeneros(request):
    generos = Genero.objects.all()
    return render(request, 'webapp/genero/listar_generos.html', {'generos': generos})

def formularioGenero(request):
    return render(request, 'webapp/genero/formulario_genero.html')

def guardarGenero(request):
    try:
        if request.method == "POST":
            genero = Genero(
                nombre=request.POST['nombre'],
            )
            genero.save()
            messages.success(request, f"Genero ({genero.nombre}) creado exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioGenero')

def eliminarGenero(request, id):
    try:
        genero = Genero.objects.get(id = id)
        genero_nombre = genero.nombre
        genero.delete()
        messages.success(request, f"Genero ({genero_nombre}) creado exitosamente")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este genero ya que está relacionado con otros registros")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarGeneros')

def edicionGenero(request, id):
    genero = Genero.objects.get(id = id)
    return render(request, 'webapp/genero/edicion_genero.html', {'genero': genero})

def editarGenero(request):
    try:
        if request.method == "POST":
            genero = Genero.objects.get(id = request.POST['id'])
            genero.nombre = request.POST['nombre']
            genero.save()
            messages.success(request, f"Genero ({genero.nombre}) editado exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarGeneros')


# JUEGOS
def listarJuegos(request):
    juegos = Juego.objects.all()
    return render(request, 'webapp/juego/listar_juegos.html', {'juegos': juegos})

def formularioJuego(request):
    generos = Genero.objects.all()
    return render(request, 'webapp/juego/formulario_juego.html', {"generos": generos})

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
            juego.generos.add(*generos)
            juego.save()
            messages.success(request, f"Juego ({juego.titulo}) guardado exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarJuegos')

def eliminarJuego(request, id):
    try:
        juego = Juego.objects.get(id = id)
        juego_titulo = juego.titulo
        juego.delete()
        messages.success(request, f"Genero ({juego_titulo}) creado exitosamente")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este juego ya que está relacionado con otros registros")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarJuegos')

def edicionJuego(request, id):
    juego = Juego.objects.get(id = id)
    generos = Genero.objects.all()
    return render(request, 'webapp/juego/edicion_juego.html', {'juego': juego, 'generos': generos})

def editarJuego(request):
    try:
        if request.method == "POST":
            juego = Juego.objects.get(id = request.POST['id'])
            juego.titulo = request.POST['titulo']
            juego.fecha_lanzamiento = request.POST['fecha_lanzamiento']
            juego.desarrollador = request.POST['desarrollador']
            juego.editor = request.POST['editor']
            juego.esrb = request.POST['esrb']
            juego.multijugador = request.POST['multijugador']
            juego.stock = request.POST['stock']
            juego.precio = request.POST['precio']
            juego.imagen = request.POST['imagen']
            juego.habilitado = request.POST['habilitado']
            juego.generos.clear()
            generos = request.POST.getlist('generos')
            juego.generos.add(*generos)
            juego.save()
            messages.success(request, f"Juego ({juego.titulo}) editado exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarJuegos')


# COMPRAS
def listarCompras(request):
    compras = Compra.objects.all()
    return render(request, 'webapp/compra/listar_compras.html', {'compras': compras})

def formularioCompra(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'webapp/compra/formulario_compra.html', {"proveedores": proveedores})

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
            messages.success(request, "Compra guardada exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarCompras')



# USUARIO-EMPLEADOS
def listarUsuariosEmpleados(request):
    usuarios = Usuario.objects.filter(rol = 'E').filter(habilitado = True)
    return render(request, 'webapp/usuario-empleado/listar_empleados.html', {'usuarios': usuarios})

def formularioUsuarioEmpleado(request):
    return render(request, 'webapp/usuario-empleado/formulario_empleado.html')

def guardarUsuarioEmpleado(request):
    try:
        if request.method == "POST":
            usuario = Usuario(
                email = request.POST['email'],
                clave = request.POST['clave'],
                rol = 'E',
                nombre = request.POST['nombre'],
                apellido = request.POST['apellido'],
                telefono = request.POST['telefono'],
                fecha_nacimiento = request.POST['fecha_nacimiento'],
            )
            usuario.save()
            messages.success(request, f"Empleado ({usuario.nombre}) guardado exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')

def deshabilitarUsuarioEmpleado(request, id):
    try:
        usuario = Usuario.objects.get(id = id)
        usuario.habilitado = False
        usuario.save()
        messages.success(request, f"Empleado ({usuario.nombre}) deshabilitado exitosamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')

def habilitarUsuarioEmpleado(request, id):
    try:
        usuario = Usuario.objects.get(id = id)
        usuario.habilitado = True
        usuario.save()
        messages.success(request, f"Empleado ({usuario.nombre}) habilitado exitosamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')

def edicionUsuarioEmpleado(request, id):
    usuario = Usuario.objects.get(id = id)
    return render(request, 'webapp/usuario-empleado/edicion_empleado.html', {'usuario': usuario})

def editarUsuarioEmpleado(request):
    try:
        if request.method == "POST":
            usuario = Usuario.objects.get(id = request.POST['id'])
            usuario.email = request.POST['email']
            usuario.nombre = request.POST['nombre']
            usuario.apellido = request.POST['apellido']
            usuario.telefono = request.POST['telefono']
            usuario.fecha_nacimiento = request.POST['fecha_nacimiento']
            usuario.save()
            messages.success(request, f"Usuario ({usuario.nombre}) ({usuario.apellido}) editado exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')

def listarUsuariosEmpleadosDeshabilitados(request):
    usuarios = Usuario.objects.filter(rol = 'E').filter(habilitado = False)
    return render(request, 'webapp/usuario-empleado/listar_empleados_desh.html', {'usuarios': usuarios})

# VENTAS
def listarVentas(request):
    ventas = Venta.objects.all()
    return render(request, 'webapp/venta/listar_ventas.html', {'ventas': ventas})

def formularioVenta(request):
    clientes = Usuario.objects.all()
    return render(request, 'webapp/venta/formulario_venta.html', {"clientes": Usuario.objects.all()})

def guardarVenta(request):
    try:
        if request.method == "POST":
            usuarioID = request.POST['usuario']
            usuario = Usuario.objects.get(id=int(usuarioID))

            venta = Venta(
                total = request.POST['total'],
                id_usuario = usuario
            )
            venta.save()
            messages.success(request, "Venta guardada exitosamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioVenta')