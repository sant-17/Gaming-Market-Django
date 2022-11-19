from django.shortcuts import render, redirect
from .models import *
from datetime import date

# Mensajes tipo cookies temporales
from django.contrib import messages

# Gestión de errores de base de datos
from django.db import IntegrityError    

# Paginador
from django.core.paginator import Paginator

#Almacenamiento de archivos
from django.core.files.storage import FileSystemStorage

# Create your views here.

def signup(request):
    return render(request, 'webapp/tienda/sign-up.html')

def guardarCliente(request):
    try:
        if request.method == "POST":
            usuario = Usuario(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                email=request.POST['email'],
                clave=request.POST['clave'],
            )
            usuario.full_clean()
            if usuario.esMayorDeEdad():
                usuario.save()
                messages.success(request, f"Su usuario ha sido creado con éxito")
            else:
                messages.warning(request, "Lo sentimos, no admitimos menores de edad")
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:index')

def login(request):
    if request.method == "POST":
        try:
            email = request.POST['email']
            clave = request.POST['clave']

            usuario = Usuario.objects.get(email = email, clave = clave)
            # Crear sesión
            request.session["logueo"] = [usuario.id, usuario.nombre, usuario.apellido, usuario.email, usuario.get_rol_display()]
            # -------------
            messages.success(request, "Bienvenido")
            return redirect('webapp:index')
        except Usuario.DoesNotExist:
            messages.warning(request, "El usuario no existe")
            return redirect('webapp:index')
        except Exception as e:
            messages.warning(request, e)
            return redirect('webapp:index')
    else:
        messages.warning(request, "Usted no ha enviado datos")
        return redirect('webapp:index')

def logout(request):
    try:
        del request.session["logueo"]
        return redirect('webapp:index')
    except Exception as e:
        messages.error(request, e)
        return redirect('webapp:index')

def index(request):
    juegos = Juego.objects.filter(habilitado = True).order_by('-id')[:3]
    return render(request, 'webapp/tienda/landing-page.html', {"juegos": juegos})

def tienda(request):
    juegos = Juego.objects.filter(habilitado = True)
    return render(request, 'webapp/tienda/productos.html', {"juegos": juegos})


# PROVEEDORES
def listarProveedores(request):
    proveedores = Proveedor.objects.order_by('-habilitado')
    paginator = Paginator(proveedores, 10)
    page_number = request.GET.get('page')

    #Sobreescribiendo la salida de la consulta
    proveedores = paginator.get_page(page_number)

    contexto = {"proveedores": proveedores}
    return render(request, 'webapp/proveedor/listar_proveedores.html', contexto)

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

def buscarProveedor(request):
    from django.db.models import Q

    if request.method == "POST":
        resultado = request.POST["buscar"]
        proveedores = Proveedor.objects.order_by('-habilitado').filter(Q(nombre__icontains = resultado) | Q(email__icontains = resultado) | Q(telefono__icontains = resultado))
        paginator = Paginator(proveedores, 10)
        page_number = request.GET.get('page')
        proveedores = paginator.get_page(page_number)
        contexto = {"proveedores" : proveedores}
        return render(request, 'webapp/proveedor/listar_proveedores_ajax.html', contexto)
    else:
        messages.error(request, "No envió datos")
        return redirect('webapp:listarProveedores')
        
# GENEROS
def listarGeneros(request):
    generos = Genero.objects.all()
    paginator = Paginator(generos, 10)
    page_number = request.GET.get('page')

    #Sobreescribiendo la salida de la consulta
    generos = paginator.get_page(page_number)

    contexto = {"generos": generos}
    return render(request, 'webapp/genero/listar_generos.html', contexto)

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
    juegos = Juego.objects.order_by('-habilitado')
    paginator = Paginator(juegos, 10)
    page_number = request.GET.get('page')

    #Sobreescribiendo la salida de la consulta
    juegos = paginator.get_page(page_number)

    return render(request, 'webapp/juego/listar_juegos.html', {'juegos': juegos})

def formularioJuego(request):
    generos = Genero.objects.all()
    proveedores = Proveedor.objects.filter(habilitado = True)
    return render(request, 'webapp/juego/formulario_juego.html', {"generos": generos, "proveedores": proveedores})

def guardarJuego(request):
    try:
        if request.method == "POST":

            if request.FILES:
                fss = FileSystemStorage()
                i = request.FILES["imagen"]
                file = fss.save("webapp/images/" + i.name, i)
            else:
                file = 'webapp/images/default.jpg'

            proveedor = Proveedor.objects.get(pk = request.POST["proveedor"])
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
                habilitado = request.POST['habilitado'],
                proveedor = proveedor,
                imagen = file

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
    proveedores = Proveedor.objects.filter(habilitado = True)
    return render(request, 'webapp/juego/edicion_juego.html', {'juego': juego, 'generos': generos, "proveedores": proveedores})

def editarJuego(request):
    try:
        if request.method == "POST":
            if request.FILES:
                fss = FileSystemStorage()
                i = request.FILES["imagen"]
                file = fss.save("webapp/images/" + i.name, i)
            else:
                juegoTemp = Juego.objects.get(id = request.POST['id'])
                file = juegoTemp.imagen
            proveedor = Proveedor.objects.get(pk = request.POST["proveedor"])
            juego = Juego.objects.get(id = request.POST['id'])
            juego.titulo = request.POST['titulo']
            juego.fecha_lanzamiento = request.POST['fecha_lanzamiento']
            juego.desarrollador = request.POST['desarrollador']
            juego.editor = request.POST['editor']
            juego.esrb = request.POST['esrb']
            juego.multijugador = request.POST['multijugador']
            juego.stock = request.POST['stock']
            juego.precio = request.POST['precio']
            juego.imagen = file
            juego.habilitado = request.POST['habilitado']
            juego.proveedor = proveedor
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

def buscarJuego(request):
    from django.db.models import Q

    if request.method == "POST":
        resultado = request.POST["buscar"]
        juegos = Juego.objects.filter(Q(titulo__icontains = resultado) | Q(desarrollador__icontains = resultado) | Q(editor__icontains = resultado))
        paginator = Paginator(juegos, 10)
        page_number = request.GET.get('page')
        juegos = paginator.get_page(page_number)
        contexto = {"juegos" : juegos}
        return render(request, 'webapp/juego/listar_juegos_ajax.html', contexto)
    else:
        messages.error(request, "No envió datos")
        return redirect('webapp:juegos')


# USUARIO-EMPLEADOS
def listarUsuariosEmpleados(request):
    usuarios = Usuario.objects.order_by('-habilitado').filter(rol = 'E')
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')

    usuarios = paginator.get_page(page_number)

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

def buscarEmpleado(request):
    from django.db.models import Q

    if request.method == "POST":
        resultado = request.POST["buscar"]
        empleados = Usuario.objects.order_by('-habilitado').filter(Q(email__icontains = resultado) | Q(nombre__icontains = resultado) | Q(apellido__icontains = resultado)).filter(rol = 'E')
        paginator = Paginator(empleados, 10)
        page_number = request.GET.get('page')
        empleados = paginator.get_page(page_number)
        contexto = {"usuarios" : empleados}
        return render(request, 'webapp/usuario-empleado/listar_empleados_ajax.html', contexto)
    else:
        messages.error(request, "No envió datos")
        return redirect('webapp:listarEmpleados')

