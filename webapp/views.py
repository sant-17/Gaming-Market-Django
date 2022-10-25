
from django.shortcuts import render, redirect
from .models import *

# Mensajes tipo cookies temporales
from django.contrib import messages

# Gestión de errores de base de datos
from django.db import IntegrityError    

# Create your views here.

def index(request):
    return render(request, 'webapp/index.html')

def listarProveedores(request):
    return render(request, 'webapp/proveedor/listar_proveedores.html', {'proveedores': Proveedor.objects.all()})

def eliminarProveedor(request, id):
    try:
        proveedor = Proveedor.objects.get(id = id)
        proveedor.delete()
    except IntegrityError:
        messages.warning(request, "No puede eliminar este proveedor ya que está relacionado con otros registros")
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
            messages.success(request, "Proveedor editado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')

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
    try:
        genero = Genero.objects.get(id = id)
        genero.delete()
    except IntegrityError:
        pass
    except Exception as e:
        pass
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

def eliminarJuego(request, id):
    try:
        juego = Juego.objects.get(id = id)
        juego.delete()
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
            for generoID in generos:
                genero = Genero.objects.get(id=int(generoID))
                juego.generos.add(genero)
            juego.save()
            messages.success(request, "Juego editado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarJuegos')

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
    return redirect('webapp:listarJuegos')

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

def listarUsuarios(request):
    return render(request, 'webapp/usuario/listar_usuarios.html', {'usuarios': Usuario.objects.all()})

def formularioUsuario(request):
    return render(request, 'webapp/usuario/formulario_usuario.html')

def guardarUsuario(request):
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
            messages.success(request, "Usuario guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioUsuario')


def listarVentas(request):
    return render(request, 'webapp/venta/listar_ventas.html', {'ventas': Venta.objects.all()})

def formularioVenta(request):
    return render(request, 'webapp/venta/formulario_venta.html', {"clientes": Cliente.objects.all()})

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
            messages.success(request, "Venta guardado correctamente")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:formularioVenta')