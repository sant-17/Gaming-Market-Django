from django.shortcuts import render, redirect

from webapp.Carrito import Carrito
from .models import *
from datetime import date
from django.db.models import Q

# Mensajes tipo cookies temporales
from django.contrib import messages

# Gestión de errores de base de datos
from django.db import IntegrityError    

# Paginador
from django.core.paginator import Paginator

#Almacenamiento de archivos
from django.core.files.storage import FileSystemStorage

#Libreria para encripación
from passlib.context import CryptContext
# Round: Iteraciones para reducir la posibilidad de cracking.
contexto = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=333
)


# Create your views here.

# TIENDA
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
                clave= contexto.hash(request.POST['clave']) ,
                
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
            clavePost = request.POST['clave']
            clave= contexto.hash(clavePost)
            
            usuario = Usuario.objects.get(email = email)
            
            if contexto.verify(clavePost, usuario.clave):
                request.session["logueoCliente"] = [usuario.id, usuario.nombre, usuario.apellido, usuario.email, usuario.get_rol_display()]       
                # -------------
                messages.success(request, "Bienvenido")
            else:
                messages.warning(request, "Contraseña incorrecta")
                
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
        del request.session["logueoCliente"]
        carrito = Carrito(request)
        carrito.limpiar()
        del request.session["final"]
        return redirect('webapp:index')
    except Exception as e:
        messages.error(request, e)
        return redirect('webapp:index')

def index(request):
    juegos = Juego.objects.filter(habilitado = True).order_by('-id')[:3]
    return render(request, 'webapp/tienda/landing-page.html', {"juegos": juegos})

def tienda(request):
    juegos = Juego.objects.filter(habilitado = True)
    paginator = Paginator(juegos, 15)
    page_number = request.GET.get('page')
    juegos = paginator.get_page(page_number)
    return render(request, 'webapp/tienda/shop.html', {"juegos": juegos})

def producto(request, id):
    try:
        juego = Juego.objects.get(id = id)
        generoPrincipal = juego.generos.first()
        recomendaciones = Juego.objects.filter(generos__id__contains=generoPrincipal.id)[:3]
        cantidad = Juego.objects.filter(generos__id__contains=generoPrincipal.id).count()
        recomendacion = "similares"
        if cantidad < 3:
            recomendaciones = Juego.objects.filter(habilitado = True).order_by('-id')[:3]
            recomendacion = "nuevos"
        return render(request, 'webapp/tienda/single-product.html', {'juego': juego, 'recomendacion': recomendacion,  'recomendaciones': recomendaciones})
    except:
        return render(request, 'webapp/tienda/404.html')

"""Carrito de compras
Método para agregar los juegos al la lista de compras
carrito: variable de sesión donde se almacenan las id de las selecciones
Returns:
    _type_: _vacio_
"""
def agregarAlCarrito(request, id):
    
    try:
        #cliente = request.session.get('logueoCliente')
        #if cliente:
        carrito = Carrito(request)
        juego = Juego.objects.get(id = id)
        
        carrito.agregar(juego)
            
        messages.warning(request, f"{request.session['carrito']} agregado {juego.titulo}")
    except Exception as e:
        messages.warning(request, f"Error: {e}")
    return redirect('webapp:tienda')

def verCarrito(request):
    try:
        cliente = request.session.get('logueoCliente', False)
        if cliente:
            
            if request.session.get("carrito"):
                carrito = request.session["carrito"]
                            
                juegos = Juego.objects.filter(id__in=carrito)
                total = 0
                for juego in juegos:
                    total += juego.precio
                return render(request, 'webapp/tienda/cart.html')  #{'juegos': juegos, 'total': total})
            else:
                return render(request, 'webapp/tienda/cart.html')
    except Exception as e:
        messages.warning(request, f"Error: {e}")
    return redirect('webapp:tienda')

def eliminarJuegoDelCarrito(request, id):
    try:
        cliente = request.session.get('logueoCliente', False)
        if cliente:
            carrito = Carrito(request)
            juego = Juego.objects.get(id = id)
            
            carrito.eliminar(juego)
            
            return redirect('webapp:verCarrito')
        else:
            messages.warning(request, "Inicia sesión primero")
            return redirect('webapp:tienda')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:tienda')

def restarJuego(request, id):
    try:
        cliente = request.session.get('logueoCliente', False)
        if cliente:
            carrito = Carrito(request)
            juego = Juego.objects.get(id = id)
            
            carrito.restar(juego)
            
            return redirect('webapp:verCarrito')
        else:
            messages.warning(request, "Inicia sesión primero")
            return redirect('webapp:tienda')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:tienda')

def vaciarCarrito(request):
    carrito = Carrito(request)    
    carrito.limpiar()
    
    return redirect('webapp:tienda')

def checkout(request):
    try:
        cliente = request.session.get('logueoCliente', False)
        if cliente:
            carrito = request.session["carrito"]
            if len(carrito) > 0:
                request.session["final"] = request.session["carrito"]
                
                juegos = Juego.objects.filter(id__in=carrito)
                total = 0
                for juego in juegos:
                    total += juego.precio
                usuario = Usuario.objects.get(id = cliente[0])
                return render(request, 'webapp/tienda/checkout.html', {'juegos': juegos, 'total': total, 'cliente': usuario})
            else:
                return redirect('webapp:verCarrito')
        else:
            messages.warning(request, "Inicia sesión primero")
            return redirect('webapp:tienda')
    except Exception as e:
        del request.session["final"]
        messages.error(request, f"Error: {e}")
    return redirect('webapp:tienda')

def venta(request):
    try:
        cliente = request.session.get('logueoCliente', False)
        idsJuegos = request.session.get('final', False)
        if cliente and idsJuegos:
            #del request.session["carrito"]
            #request.session["carrito"] = []
            juegos = Juego.objects.filter(id__in=idsJuegos)
            total = 0
            cliente = Usuario.objects.get(id = cliente[0])
            for juego in juegos:
                total += juego.precio
            venta = Venta(
                id_usuario = cliente,
                total = total
            )
            venta.save()
            for juego in juegos:
                venta_detalle = Venta_detalle(
                    id_juego = juego,
                    id_venta = venta,
                    precio = juego.precio
                )
                venta_detalle.save()
            del request.session["final"]
            messages.success(request, "Tu compra ha sido un éxito")
        if cliente and not idsJuegos:
            messages.warning(request, "Complete la compra a travez del checkout")
        if idsJuegos and not cliente:
            messages.warning(request, "Inicie sesión")
        return redirect('webapp:tienda')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    del request.session["final"]
    return redirect('webapp:tienda')

# CRUD

def formLoginCrud(request):
    return render(request, 'webapp/crud/login.html')

def loginCrud(request):
    try:
        if request.method == "POST":
            
            email = request.POST['email']
            clavePost = request.POST['clave']
            
            usuario = Usuario.objects.get(email = email)
            
            if contexto.verify(clavePost, usuario.clave):                
                if usuario.rol == 'C':
                    messages.error(request, "Este usuario no posee permisos para ingresar")
                    return redirect('webapp:loginEmpleados')
                #Crear sesión
                request.session["logueo"] = [usuario.id, usuario.nombre, usuario.apellido, usuario.email, usuario.get_rol_display()]

                logueo = request.session.get("logueo", False)
                # -------------
                return redirect('webapp:inicioCrud')
            else:
                 messages.warning(request, "Contraseña incorrecta")
        else:
            messages.warning(request, "Usted no ha enviado datos")
            return redirect('webapp:loginEmpleados')
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe")
        return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('webapp:loginEmpleados')

def logoutCrud(request):
    try:
        del request.session["logueo"]
        return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, e)
        return redirect('webapp:loginEmpleados')

def inicioCrud(request):
    return render(request, 'webapp/crud/index.html')

# PROVEEDORES
def listarProveedores(request):

    login = request.session.get('logueo', False)

    if login:
        proveedores = Proveedor.objects.order_by('-habilitado')
        paginator = Paginator(proveedores, 10)
        page_number = request.GET.get('page')

        #Sobreescribiendo la salida de la consulta
        proveedores = paginator.get_page(page_number)

        contexto = {"proveedores": proveedores}
        return render(request, 'webapp/proveedor/listar_proveedores.html', contexto)
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def formularioProveedor(request):
    login = request.session.get('logueo', False)
    if login:
        return render(request, 'webapp/proveedor/formulario_proveedor.html')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def guardarProveedor(request):
    try:
        login = request.session.get('logueo', False)
        if login:
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
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')

def deshabilitarProveedor(request, id):
    try:
        login = request.session.get('logueo', False)
        if login:
            proveedor = Proveedor.objects.get(id = id)
            proveedor.habilitado = False
            proveedor.save()
            messages.success(request, f"Proveedor ({proveedor.nombre}) deshabilitado exitosamente")
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')

def habilitarProveedor(request, id):
    try:
        login = request.session.get('logueo', False)
        if login:
            proveedor = Proveedor.objects.get(id = id)
            proveedor.habilitado = True
            proveedor.save()
            messages.success(request, f"Proveedor ({proveedor.nombre}) habilitado exitosamente")
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')

def edicionProveedor(request, id):
    login = request.session.get('logueo', False)
    if login:
        proveedor = Proveedor.objects.get(id = id)
        return render(request, 'webapp/proveedor/edicion_proveedor.html', {'proveedor': proveedor})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def editarProveedor(request):
    try:
        login = request.session.get('logueo', False)
        if login:
            if request.method == "POST":
                proveedor = Proveedor.objects.get(id = request.POST['id'])
                proveedor.nombre = request.POST['nombre']
                proveedor.email = request.POST['email']
                proveedor.telefono = request.POST['telefono']
                proveedor.save()
                messages.success(request, f"Proveedor ({proveedor.nombre}) editado exitosamente")
            else:
                messages.warning(request, "Usted no ha enviado datos")
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')

def buscarProveedor(request):
    try:
        login = request.session.get('logueo', False)
        if login:
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
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')
    
        
# GENEROS
def listarGeneros(request):
    login = request.session.get('logueo', False)
    if login:
        generos = Genero.objects.all()
        paginator = Paginator(generos, 10)
        page_number = request.GET.get('page')
        generos = paginator.get_page(page_number)
        contexto = {"generos": generos}
        return render(request, 'webapp/genero/listar_generos.html', contexto)
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def formularioGenero(request):
    login = request.session.get('logueo', False)
    if login:
        return render(request, 'webapp/genero/formulario_genero.html')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def guardarGenero(request):
    try:
        login = request.session.get('logueo', False)
        if login:
            if request.method == "POST":
                genero = Genero(
                    nombre=request.POST['nombre'],
                )
                genero.save()
                messages.success(request, f"Genero ({genero.nombre}) creado exitosamente")
            else:
                messages.warning(request, "Usted no ha enviado datos")
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarGeneros')

def eliminarGenero(request, id):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "A":
                genero = Genero.objects.get(id = id)
                genero_nombre = genero.nombre
                genero.delete()
                messages.success(request, f"Genero ({genero_nombre}) eliminado con éxito")
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción")
                return redirect('webapp:listarGeneros')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except IntegrityError:
        messages.warning(request, "No puede eliminar este genero ya que está relacionado con otros registros")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarGeneros')

def edicionGenero(request, id):
    login = request.session.get('logueo', False)
    if login:
        genero = Genero.objects.get(id = id)
        return render(request, 'webapp/genero/edicion_genero.html', {'genero': genero})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def editarGenero(request):
    try:
        login = request.session.get('logueo', False)
        if login:
            if request.method == "POST":
                genero = Genero.objects.get(id = request.POST['id'])
                genero.nombre = request.POST['nombre']
                genero.save()
                messages.success(request, f"Genero ({genero.nombre}) editado exitosamente")
            else:
                messages.warning(request, "Usted no ha enviado datos")
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarGeneros')


# JUEGOS
def listarJuegos(request):
    login = request.session.get('logueo', False)
    if login:
        juegos = Juego.objects.order_by('-habilitado')
        paginator = Paginator(juegos, 10)
        page_number = request.GET.get('page')
        juegos = paginator.get_page(page_number)
        return render(request, 'webapp/juego/listar_juegos.html', {'juegos': juegos})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def formularioJuego(request):
    login = request.session.get('logueo', False)
    if login:
        generos = Genero.objects.all()
        proveedores = Proveedor.objects.filter(habilitado = True)
        return render(request, 'webapp/juego/formulario_juego.html', {"generos": generos, "proveedores": proveedores})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def guardarJuego(request):
    try:
        login = request.session.get('logueo', False)
        if login:
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
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarJuegos')

def eliminarJuego(request, id):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "A":
                juego = Juego.objects.get(id = id)
                juego_titulo = juego.titulo
                juego.delete()
                messages.success(request, f"Genero ({juego_titulo}) creado exitosamente")
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción")
                return redirect('webapp:listarJuegos')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except IntegrityError:
        messages.warning(request, "No puede eliminar este juego ya que está relacionado con otros registros")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarJuegos')

def edicionJuego(request, id):
    login = request.session.get('logueo', False)
    if login:
        juego = Juego.objects.get(id = id)
        generos = Genero.objects.all()
        proveedores = Proveedor.objects.filter(habilitado = True)
        return render(request, 'webapp/juego/edicion_juego.html', {'juego': juego, 'generos': generos, "proveedores": proveedores})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def editarJuego(request):
    try:
        login = request.session.get('logueo', False)
        if login:
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
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarJuegos')

def buscarJuego(request):
    try:
        login = request.session.get('logueo', False)
        if login:
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
                return redirect('webapp:listarJuegos')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarJuegos')


# USUARIO-EMPLEADOS
def listarUsuariosEmpleados(request):
    login = request.session.get('logueo', False)
    if login:
        if login[4] == "Administrador":
            usuarios = Usuario.objects.order_by('-habilitado').filter(rol = 'E')
            paginator = Paginator(usuarios, 10)
            page_number = request.GET.get('page')
            usuarios = paginator.get_page(page_number)
            return render(request, 'webapp/usuario-empleado/listar_empleados.html', {'usuarios': usuarios})
        else:
            messages.warning(request, f"{login[4]}")
            return redirect('webapp:inicioCrud')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def formularioUsuarioEmpleado(request):
    login = request.session.get('logueo', False)
    if login:
        if login[4] == "A":
            return render(request, 'webapp/usuario-empleado/formulario_empleado.html')
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('webapp:inicioCrud')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def guardarUsuarioEmpleado(request):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "A":
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
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('webapp:inicioCrud')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')

def deshabilitarUsuarioEmpleado(request, id):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "A":
                usuario = Usuario.objects.get(id = id)
                usuario.habilitado = False
                usuario.save()
                messages.success(request, f"Empleado ({usuario.nombre}) deshabilitado exitosamente")
                return redirect('webapp:listarEmpleados')
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('webapp:inicioCrud')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')

def habilitarUsuarioEmpleado(request, id):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "A":
                usuario = Usuario.objects.get(id = id)
                usuario.habilitado = True
                usuario.save()
                messages.success(request, f"Empleado ({usuario.nombre}) habilitado exitosamente")
                return redirect('webapp:listarEmpleados')
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('webapp:inicioCrud')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')

def edicionUsuarioEmpleado(request, id):
    login = request.session.get('logueo', False)
    if login:
        if login[4] == "A":
            usuario = Usuario.objects.get(id = id)
            return render(request, 'webapp/usuario-empleado/edicion_empleado.html', {'usuario': usuario})
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('webapp:inicioCrud')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

def editarUsuarioEmpleado(request):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "A":
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
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('webapp:inicioCrud')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')

def buscarEmpleado(request):
    login = request.session.get('logueo', False)
    if login:
        if login[4] == "A":
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
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('webapp:inicioCrud')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')