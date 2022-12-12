from email.policy import HTTP
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect

from webapp.carrito import Carrito
from .models import *
from datetime import date
from django.db.models import Q
from gaming_market import settings
from decouple import config

# Mensajes tipo cookies temporales
from django.contrib import messages

# Gestión de errores de base de datos
from django.db import IntegrityError

# Paginador
from django.core.paginator import Paginator

# Almacenamiento de archivos
from django.core.files.storage import FileSystemStorage

# Libreria para encripación
from passlib.context import CryptContext
# Round: Iteraciones para reducir la posibilidad de cracking.
contexto = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=333
)
# para la gestión de correos

# Create your views here.

# TIENDA


def signup(request):
    """
    **inicio de sesión**

    Returns:
        _type_:  rendeiza la pagina sig-up.html
    """
    return render(request, 'webapp/tienda/sign-up.html')


def guardarCliente(request):
    """ 
    **Guardar cliente**
        Recive por medio de POST los datos del formulario, con el fin de crear nuevo cliente

    Args:
        request (_HttpRequest_): _Datos sobre la sesión en la que estamos trabajando

    Returns:
        objeto cliente
    """
    try:

        if request.method == "POST":
            usuario = Usuario(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                email=request.POST['email'],
                clave=contexto.hash(request.POST['clave']),

            )
            usuario.full_clean()
            if usuario.esMayorDeEdad():
                usuario.save()
                messages.success(
                    request, f"Su usuario ha sido creado con éxito")
            else:
                messages.warning(
                    request, "Lo sentimos, no admitimos menores de edad")
                return redirect('webapp:signup')
        else:
            messages.warning(request, "Usted no ha enviado datos")
    except Exception as e:
        messages.error(request, f"Error: Ya existe un usuario con este correo")
        return redirect('webapp:signup')
    return redirect('webapp:index')


def login(request):
    """
    **Formulario para el logueo de usuarios**

    Args:
        request (_type_): Datos sobre la sesión en la que estamos trabajando

    Returns:
        _redirect_: _Redirección a pagina de inicio
    """
    if request.method == "POST":
        try:
            user = Usuario.objects.get(email=request.POST['email'])
            if user.rol == 'C':
                email = request.POST['email']
                clavePost = request.POST['clave']
                clave = contexto.hash(clavePost)

                usuario = Usuario.objects.get(email=email)

                if contexto.verify(clavePost, usuario.clave):
                    request.session["logueoCliente"] = [
                        usuario.id, usuario.nombre, usuario.apellido, usuario.email, usuario.get_rol_display()]
                    # -------------
                    cliente = request.session.get('logueoCliente', False)
                    subjet = 'Inicio de sesión' + cliente[1]
                    message = "Bienbenido"+" " + cliente[2]
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ["osernam@gmail.com"]

                    send_mail(subjet, message, email_from, recipient_list)
                    
                    messages.success(request, "Bienvenido")
            else:
                messages.warning(request, "Contraseña incorrecta")

            if user.rol != 'C':
                if request.method == "POST":

                    email = request.POST['email']
                    clavePost = request.POST['clave']

                    usuario = Usuario.objects.get(email=email)

                    if contexto.verify(clavePost, usuario.clave):
                        if usuario.rol == 'C':
                            messages.error(
                                request, "Este usuario no posee permisos para ingresar")
                            return redirect('webapp:loginEmpleados')
                            # Crear sesión
                        request.session["logueo"] = [
                                usuario.id, usuario.nombre, usuario.apellido, usuario.email, usuario.get_rol_display()]

                        logueo = request.session.get("logueo", False)
                        # -------------
                        return redirect('webapp:inicioCrud')
                    else:
                            messages.warning(request, "Contraseña incorrecta")
                else:
                    messages.warning(request, "Usted no ha enviado datos")
                    return redirect('webapp:loginEmpleados')

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
    """ 
    **Cerrar seción**
        Reinicia las variables de seción de modo que borra los datos de la seción

    Args:
        request (_HttpRequest_): _Datos sobre la seción en la que estamos trabajando
        logueoCliente (request.session): seción actual
        carrito (request.session): carrito de compras

    Returns:
        logueoCliente: vacio
        carrito: vacio
    """
    try:
        
        
        del request.session["logueoCliente"]
        del request.session["logueo"]
        carrito = Carrito(request)
        carrito.limpiar()
        del request.session["final"]
        return redirect('webapp:index')
    except Exception as e:
        messages.error(request, e)
        return redirect('webapp:index')


def index(request):
    """Pagina de inicio

    Args:
        request (_type_): _seción actual_

    Returns:

        html: landin page con los juegos(lista) más recientes
    """
    try:
        if request.session["logueo"]:
            request.session["logueoCliente"] = request.session["logueo"] 
        juegos = Juego.objects.filter(habilitado=True).order_by('-id')[:3]
        
        return render(request, 'webapp/tienda/landing-page.html', {"juegos": juegos})
    except Exception as e:
        messages.error(request, e)
        juegos = Juego.objects.filter(habilitado=True).order_by('-id')[:3]
        return render(request, 'webapp/tienda/landing-page.html', {"juegos": juegos})

# RESTABLECER CLAVE


def mostrarRestablecer(request):
    """Renderiza el formulario para ingresar el correo de restablecimiento

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return render(request, 'webapp/resetClave/clave_reset_formulario.html')


def cambiarClave(request, id):
    """Recive el id del cliente desde el correo y renderiza el formulario para actualizar la clave

    Args:
        request (_type_): _description_
        id (_int_): id del cliente

    Returns:
        _type_: _description_
    """
    return render(request, 'webapp/resetClave/clave_reset_confirmacion.html', {"id": id})


def cambiarPws(request):
    """Recive la nueva clave

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        if request.method == "POST":
            usuario = Usuario.objects.get(id=request.POST['id'])
            clave = request.POST['clave']
            usuario.clave = contexto.hash(clave)
            usuario.save()

            messages.success(request, "Cambio de contraseña exitoso ")
        else:
            messages.warning(
                request, "No se enviaron los datos correctamente ")

    except Exception as e:
        messages.error(request, f"error: {e}")

    return redirect('webapp:index')


def restablecer(request):
    """Recibe el correo al cual se enviara el enlace de recuperación

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        if request.method == "POST":
            emailRecuperation = request.POST["correo"]
            usuario = Usuario.objects.get(email=emailRecuperation)
            #contexto.verify(clavePost, usuario.clave)
            #message = "Atraves del siguiente enlace podra restablecer su contraseña: \n"+"{config('protocol')}://{ config('domain')}{%'webapp/resetClave/clave_reset_confirmacion.html' uidb64=uid token=token%}"+str(usuario.pk)

            subjet = 'Solicitud de cambio de contraseña'
            message = "A traves del siguiente enlace podra restablecer su contraseña: \n" + \
                "http://127.0.0.1:8000/webapp/reset/clave/"+str(usuario.pk)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [emailRecuperation]

            send_mail(subjet, message, email_from,
                      recipient_list, fail_silently=False)
            messages.info(
                request, 'Correo enviado, revisa tu bandeja de entrada')
    except Exception as e:
        messages.error(request, f"error: {e}")

    return redirect('webapp:index')


def tienda(request):
    """Vista donde estan los juegos disponibles para comprar

    Args:
        request (_type_): _seción actual_

    Returns:
        html: landin page con los juegos(lista) habilitados
    """
    juegos = Juego.objects.filter(habilitado=True)
    paginator = Paginator(juegos, 15)
    page_number = request.GET.get('page')
    juegos = paginator.get_page(page_number)
    return render(request, 'webapp/tienda/shop.html', {"juegos": juegos})


def producto(request, id):
    """Al momento de crear un nuevo juego, genera recomendaciones en vase a los generos 

    Args:
        request (_type_): _seción actual_
        id (int): identificador del juego

    Returns:
        _html_: _template con la lista de juegos similares y lista de recomendados_
    """
    try:
        juego = Juego.objects.get(id=id)
        generoPrincipal = juego.generos.first()
        recomendaciones = Juego.objects.filter(
            generos__id__contains=generoPrincipal.id)[:3]
        cantidad = Juego.objects.filter(
            generos__id__contains=generoPrincipal.id).count()
        recomendacion = "similares"
        if cantidad < 3:
            recomendaciones = Juego.objects.filter(
                habilitado=True).order_by('-id')[:3]
            recomendacion = "nuevos"
        return render(request, 'webapp/tienda/single-product.html', {'juego': juego, 'recomendacion': recomendacion,  'recomendaciones': recomendaciones})
    except:
        return render(request, 'webapp/tienda/404.html')


def agregarAlCarrito(request, id):
    """Carrito de compras
        Método para agregar los juegos al la lista de compras
        Args:
            request (_type_): _seción actual_
            id (int): identificador del juego
        Returns:
            _type_: _vacio_
    """
    try:
        #cliente = request.session.get('logueoCliente')
        # if cliente:
        carrito = Carrito(request)
        juego = Juego.objects.get(id=id)

        carrito.agregar(juego)

        messages.warning(
            request, f"{request.session['carrito']} agregado {juego.titulo}")
    except Exception as e:
        messages.warning(request, f"Error: {e}")
    return redirect('webapp:tienda')


def aumentarEnCarrito(request, id):
    """Aumenta en el carrito 1 unidad

    Args:
        request (_type_): _seción actual_
        id (int): identificador del juego

    Returns:
        _html_: _aumento de 1 unidad_
    """
    try:
        #cliente = request.session.get('logueoCliente')
        # if cliente:
        carrito = Carrito(request)
        juego = Juego.objects.get(id=id)

        carrito.agregar(juego)

        if carrito.stocks(juego):   
            messages.warning( request, f"No hay stock de {juego.titulo}")
        messages.warning(
            request, f"{request.session['carrito']} agregado {juego.titulo}")
    except Exception as e:
        messages.warning(request, f"Error: {e}")
    return redirect('webapp:verCarrito')


def verCarrito(request):
    try:
        cliente = request.session.get('logueoCliente', False)
        if cliente:

            if request.session.get("carrito"):
                carrito = request.session["carrito"]

                juegos = Juego.objects.filter(id__in=carrito)

                total = 0
                for key, value in request.session["carrito"].items():
                    total += float(value["precio"])

                return render(request, 'webapp/tienda/cart.html', {'total': total})
            else:
                return render(request, 'webapp/tienda/cart.html')
    except Exception as e:
        messages.warning(request, f"Error: {e}")
    return redirect('webapp:verCarrito')


def eliminarJuegoDelCarrito(request, id):
    try:
        cliente = request.session.get('logueoCliente', False)
        if cliente:
            carrito = Carrito(request)
            juego = Juego.objects.get(id=id)

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
            juego = Juego.objects.get(id=id)

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

                for key, value in request.session["carrito"].items():
                    total += float(value["precio"])
                usuario = Usuario.objects.get(id=cliente[0])

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
        carrito = request.session["carrito"]

        if cliente and idsJuegos:
            ''' #del request.session["carrito"]
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
                    cantidad = carrito['cantidad'],
                    precio = juego.precio
                ) '''
            cliente = Usuario.objects.get(id=cliente[0])
            totalV = 0
            for key, value in request.session["carrito"].items():
                totalV += float(value["precio"])

            venta = Venta(
                id_usuario=cliente,
                total=totalV
            )
            venta.save()
            print("---------------------------")
            for clave, valor in carrito.items():
                print("Imprimiendo ----------->", valor["cantidad"])
                juego = Juego.objects.get(id=valor["juegoId"])
                # VERIFICAR QUE HAYA SUFICIENTE CANTIDAD DE UN PRODUCTO
                
                # RESTAR CANTIDAD DEL STOCK DEL JUEGO
                if juego.stock >= valor["cantidad"]:
                    juego.stock= juego.stock - valor["cantidad"]
                    
                    if juego.stock == 0:
                        juego.habilitado = False
                    juego.save()
                # SI EL STOCK QUEDA = 0 ENTONCES CAMBIAR ESTADO A DESHABILITADO
                    venta_detalle = Venta_detalle(
                        id_juego=juego,
                        id_venta=venta,
                        cantidad=valor["cantidad"],
                        precio=valor["precio"]
                    )
                venta_detalle.save()

                cliente = request.session.get('logueoCliente', False)
                subjet = 'Resumen de compra:'
                message = 'Resumen de compra: \n' +' '
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [cliente[3]]

                send_mail(subjet, message, email_from, recipient_list)

            carrito = Carrito(request)
            carrito.limpiar()
            del request.session["final"]
            messages.success(request, "Tu compra ha sido un éxito")
        if cliente and not idsJuegos:
            messages.warning(
                request, "Complete la compra a travez del checkout")
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

            usuario = Usuario.objects.get(email=email)

            if contexto.verify(clavePost, usuario.clave):
                if usuario.rol == 'C':
                    messages.error(
                        request, "Este usuario no posee permisos para ingresar")
                    return redirect('webapp:loginEmpleados')
                # Crear sesión
                request.session["logueo"] = [usuario.id, usuario.nombre,
                                             usuario.apellido, usuario.email, usuario.get_rol_display()]

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
        return redirect('webapp:index')
    except Exception as e:
        messages.error(request, e)
        return redirect('webapp:index')


def inicioCrud(request):
    return render(request, 'webapp/crud/index.html')

# PROVEEDORES


def listarProveedores(request):

    login = request.session.get('logueo', False)

    if login:
        proveedores = Proveedor.objects.order_by('-habilitado')
        paginator = Paginator(proveedores, 10)
        page_number = request.GET.get('page')

        # Sobreescribiendo la salida de la consulta
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
                messages.success(
                    request, f"Proveedor ({proveedor.nombre}) creado exitosamente")
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
            proveedor = Proveedor.objects.get(id=id)
            proveedor.habilitado = False
            proveedor.save()
            messages.success(
                request, f"Proveedor ({proveedor.nombre}) deshabilitado exitosamente")
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
            proveedor = Proveedor.objects.get(id=id)
            proveedor.habilitado = True
            proveedor.save()
            messages.success(
                request, f"Proveedor ({proveedor.nombre}) habilitado exitosamente")
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarProveedores')


def edicionProveedor(request, id):
    login = request.session.get('logueo', False)
    if login:
        proveedor = Proveedor.objects.get(id=id)
        return render(request, 'webapp/proveedor/edicion_proveedor.html', {'proveedor': proveedor})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')


def editarProveedor(request):
    try:
        login = request.session.get('logueo', False)
        if login:
            if request.method == "POST":
                proveedor = Proveedor.objects.get(id=request.POST['id'])
                proveedor.nombre = request.POST['nombre']
                proveedor.email = request.POST['email']
                proveedor.telefono = request.POST['telefono']
                proveedor.save()
                messages.success(
                    request, f"Proveedor ({proveedor.nombre}) editado exitosamente")
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
                proveedores = Proveedor.objects.order_by('-habilitado').filter(
                    Q(nombre__icontains=resultado) | Q(email__icontains=resultado) | Q(telefono__icontains=resultado))
                paginator = Paginator(proveedores, 10)
                page_number = request.GET.get('page')
                proveedores = paginator.get_page(page_number)
                contexto = {"proveedores": proveedores}
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
                messages.success(
                    request, f"Genero ({genero.nombre}) creado exitosamente")
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
                genero = Genero.objects.get(id=id)
                genero_nombre = genero.nombre
                genero.delete()
                messages.success(
                    request, f"Genero ({genero_nombre}) eliminado con éxito")
            else:
                messages.warning(
                    request, "No posee los permisos para hacer esa acción")
                return redirect('webapp:listarGeneros')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except IntegrityError:
        messages.warning(
            request, "No puede eliminar este genero ya que está relacionado con otros registros")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarGeneros')


def edicionGenero(request, id):
    login = request.session.get('logueo', False)
    if login:
        genero = Genero.objects.get(id=id)
        return render(request, 'webapp/genero/edicion_genero.html', {'genero': genero})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')


def editarGenero(request):
    try:
        login = request.session.get('logueo', False)
        if login:
            if request.method == "POST":
                genero = Genero.objects.get(id=request.POST['id'])
                genero.nombre = request.POST['nombre']
                genero.save()
                messages.success(
                    request, f"Genero ({genero.nombre}) editado exitosamente")
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
        proveedores = Proveedor.objects.filter(habilitado=True)
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

                proveedor = Proveedor.objects.get(pk=request.POST["proveedor"])
                juego = Juego(
                    titulo=request.POST['titulo'],
                    fecha_lanzamiento=request.POST['fecha_lanzamiento'],
                    desarrollador=request.POST['desarrollador'],
                    editor=request.POST['editor'],
                    descripcion=request.POST['descripcion'],
                    esrb=request.POST['esrb'],
                    multijugador=request.POST['multijugador'],
                    stock=request.POST['stock'],
                    precio=request.POST['precio'],
                    habilitado=request.POST['habilitado'],
                    proveedor=proveedor,
                    imagen=file

                )
                juego.save()
                generos = request.POST.getlist('generos')
                juego.generos.add(*generos)
                juego.save()
                messages.success(
                    request, f"Juego ({juego.titulo}) guardado exitosamente")
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
                juego = Juego.objects.get(id=id)
                juego_titulo = juego.titulo
                juego.delete()
                messages.success(
                    request, f"Genero ({juego_titulo}) creado exitosamente")
            else:
                messages.warning(
                    request, "No posee los permisos para hacer esa acción")
                return redirect('webapp:listarJuegos')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except IntegrityError:
        messages.warning(
            request, "No puede eliminar este juego ya que está relacionado con otros registros")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarJuegos')


def edicionJuego(request, id):
    login = request.session.get('logueo', False)
    if login:
        juego = Juego.objects.get(id=id)
        generos = Genero.objects.all()
        proveedores = Proveedor.objects.filter(habilitado=True)
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
                    juegoTemp = Juego.objects.get(id=request.POST['id'])
                    file = juegoTemp.imagen
                proveedor = Proveedor.objects.get(pk=request.POST["proveedor"])
                juego = Juego.objects.get(id=request.POST['id'])
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
                messages.success(
                    request, f"Juego ({juego.titulo}) editado exitosamente")
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
                juegos = Juego.objects.filter(Q(titulo__icontains=resultado) | Q(
                    desarrollador__icontains=resultado) | Q(editor__icontains=resultado))
                paginator = Paginator(juegos, 10)
                page_number = request.GET.get('page')
                juegos = paginator.get_page(page_number)
                contexto = {"juegos": juegos}
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
            usuarios = Usuario.objects.filter(Q(rol='E') | Q(rol='A'))
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
        if login[4] == "Administrador":
            return render(request, 'webapp/usuario-empleado/formulario_empleado.html')
        else:
            messages.warning(
                request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('webapp:inicioCrud')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')


def guardarUsuarioEmpleado(request):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "Administrador":
                if request.method == "POST":
                    usuario = Usuario(
                        email=request.POST['email'],
                        clave=request.POST['clave'],
                        rol='E',
                        nombre=request.POST['nombre'],
                        apellido=request.POST['apellido'],
                        telefono=request.POST['telefono'],
                        fecha_nacimiento=request.POST['fecha_nacimiento'],
                    )
                    usuario.save()
                    messages.success(
                        request, f"Empleado ({usuario.nombre}) guardado exitosamente")
                else:
                    messages.warning(request, "Usted no ha enviado datos")
            else:
                messages.warning(
                    request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('webapp:inicioCrud')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')


def deshabilitarUsuario(request, id):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "Administrador":
                usuario = Usuario.objects.get(id=id)
                usuario.habilitado = False
                usuario.save()
                messages.success(
                    request, f"Usuario ({usuario.nombre}) deshabilitado exitosamente")

                if usuario.rol == "C":
                    return redirect('webapp:listarClientes')
                else:
                    return redirect('webapp:listarEmpleados')
            else:
                messages.warning(
                    request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('webapp:inicioCrud')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarEmpleados')


def habilitarUsuario(request, id):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "Administrador":
                usuario = Usuario.objects.get(id=id)
                usuario.habilitado = True
                usuario.save()
                messages.success(
                    request, f"Usuario ({usuario.nombre}) habilitado exitosamente")
                if usuario.rol == "C":
                    return redirect('webapp:listarClientes')
                else:
                    return redirect('webapp:listarEmpleados')
            else:
                messages.warning(
                    request, "No posee los permisos para hacer esa acción. Contacte un administrador")
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
        if login[4] == "Administrador":
            usuario = Usuario.objects.get(id=id)
            return render(request, 'webapp/usuario-empleado/edicion_empleado.html', {'usuario': usuario})
        else:
            messages.warning(
                request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('webapp:inicioCrud')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')


def editarUsuarioEmpleado(request):
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "Administrador":
                if request.method == "POST":
                    usuario = Usuario.objects.get(id=request.POST['id'])
                    usuario.email = request.POST['email']
                    usuario.nombre = request.POST['nombre']
                    usuario.apellido = request.POST['apellido']
                    usuario.telefono = request.POST['telefono']
                    usuario.fecha_nacimiento = request.POST['fecha_nacimiento']
                    usuario.habilitado = request.POST['estado']
                    usuario.save()
                    messages.success(
                        request, f"Usuario ({usuario.nombre}) ({usuario.apellido}) editado exitosamente")
                else:
                    messages.warning(request, "Usted no ha enviado datos")
            else:
                messages.warning(
                    request, "No posee los permisos para hacer esa acción. Contacte un administrador")
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
                empleados = Usuario.objects.order_by('-habilitado').filter(Q(email__icontains=resultado) | Q(
                    nombre__icontains=resultado) | Q(apellido__icontains=resultado)).filter(rol='E')
                paginator = Paginator(empleados, 10)
                page_number = request.GET.get('page')
                empleados = paginator.get_page(page_number)
                contexto = {"usuarios": empleados}
                return render(request, 'webapp/usuario-empleado/listar_empleados_ajax.html', contexto)
            else:
                messages.error(request, "No envió datos")
                return redirect('webapp:listarEmpleados')
        else:
            messages.warning(
                request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('webapp:inicioCrud')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')

# Cliente


def miPerfil(request):
    try:
        login = request.session.get('logueoCliente', False)
        if login:
            cliente = Usuario.objects.get(id=login[0])
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return render(request, 'webapp/perfil-usuario/misDatos.html', {"cliente": cliente})


def edicionUsuarioCliente(request, id):
    login = request.session.get('logueo', False)
    if login:
        if login[4] == "Administrador":
            usuario = Usuario.objects.get(id=id)
            return render(request, 'webapp/usuario-empleado/edicion_cliente.html', {'usuario': usuario})
        else:
            messages.warning(
                request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('webapp:inicioCrud')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('webapp:loginEmpleados')


def editarUsuarioCliente(request):
    """Permite al cliente guardar los datos de la edición 

    Args:
        request (_type_): sesión actual

    Returns:
        _type_: _description_
    """
    try:
        login = request.session.get('logueoCliente', False)

        if login:

            if login[4] == "Cliente":

                if request.method == "POST":
                    usuario = Usuario.objects.get(id=login[0])
                    usuario.email = request.POST['email']
                    usuario.nombre = request.POST['nombre']
                    usuario.apellido = request.POST['apellido']
                    usuario.fecha_nacimiento = request.POST['fecha_nacimiento']
                    usuario.save()
                    messages.success(
                        request, f"Usuario ({usuario.nombre}) ({usuario.apellido}) editado exitosamente")

                else:
                    messages.warning(request, "Usted no ha enviado datos")

            else:
                messages.warning(request, "Inicie sesión primero")
                return redirect('webapp:index')
        else:
            messages.warning(
                request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('webapp:perfilCliente')

    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:tienda')


def editarCliente(request):
    # Administrador
    try:
        log = request.session.get('logueo', False)
        if log:
            if log[4] == "Administrador":

                # if request.POST['email'] != usuario.email:
                #       usuario.email = request.POST['email']
                # elif request.POST['email'] in Usuario.objects.order_by('-habilitado').filter(email = request.POST['email']):
                #       messages.success(request, f"El correo ({request.POST['email']}) ya esta en uso")
                if request.method == "POST":
                    iden = request.POST['id']
                    usuario = Usuario.objects.get(id=iden)
                    usuario.nombre = request.POST['nombre']
                    usuario.apellido = request.POST['apellido']
                    usuario.telefono = request.POST['telefono']
                    usuario.fecha_nacimiento = request.POST['fecha_nacimiento']
                    #usuario.rol = request.POST['rol']
                    usuario.habilitado = request.POST['estado']
                    usuario.save()
                    messages.success(
                        request, f"Usuario ({usuario.nombre}) ({usuario.apellido}) editado exitosamente")

                else:
                    messages.warning(request, "Usted no ha enviado datos")
            else:
                messages.warning(request, "Inicie sesión primero")
                return redirect('webapp:listarClientes')
        else:
            messages.warning(
                request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('webapp:loginEmpleados')

    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarClientes')


def buscarJuegoCli(request):
    """Buscador de juegos para vista de cliente

    Args:
        request (_type_): _description_

    Returns:
        _html_: template con lista que cumple la condición buscada
    """
    try:
        login = request.session.get('logueoCliente', False)
        if login:
            if request.method == "POST":
                resultado = request.POST["buscar"]
                juegos = Juego.objects.filter(Q(titulo__icontains=resultado) | Q(
                    desarrollador__icontains=resultado) | Q(editor__icontains=resultado))
                paginator = Paginator(juegos, 10)
                page_number = request.GET.get('page')
                juegos = paginator.get_page(page_number)
                contexto = {"juegos": juegos}
                return render(request, 'webapp/tienda/shop_ajax.html', contexto)
            else:
                messages.error(request, "No envió datos")
                return redirect('webapp:tienda')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:login')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:tienda')


def listarClientes(request):
    """Permite listar los clientes desde la seción del administrador

    Args:
        request (_type_): sesión actual

    Returns:
        list: lista de usuarios que cumplen con la condición de ser clientes
    """
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "Administrador":
                usuarios = Usuario.objects.filter(rol='C')
                paginator = Paginator(usuarios, 10)
                page_number = request.GET.get('page')
                usuarios = paginator.get_page(page_number)
                return render(request, 'webapp/usuario-empleado/listar_clientes.html', {'usuarios': usuarios})
            else:
                messages.warning(request, f"{login[4]}")
                return redirect('webapp:inicioCrud')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:tienda')


def listarVentas(request, id):
    """Permite listar las ventas desde la seción del administrador

    Args:
        request (_type_): sesión actual
        id():identificador del cliente a consultar las ventas
    Returns:
        list: lista de ventas que cumplen con la condición 
    """
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "Administrador":

                ventas = Venta.objects.filter(id_usuario__id=id)
                paginator = Paginator(ventas, 10)
                page_number = request.GET.get('page')
                ventas = paginator.get_page(page_number)

                return render(request, 'webapp/ventas/listar_ventas.html', {'ventas': ventas})
            else:
                messages.warning(request, f"{login[4]} error")
                return redirect('webapp:inicioCrud')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarClientes')


def verVenta(request, id):
    """Permite ver resumen de la venta, productos adquiridos y relaciones

    Args:
        request (_type_): sesión actual
    Returns:
        _list_: lista de juegos adquiridos en la compra
    """
    try:
        login = request.session.get('logueo', False)
        if login:
            if login[4] == "Administrador":

                ventas = Venta_detalle.objects.filter(id_venta__id=id)
                paginator = Paginator(ventas, 10)
                page_number = request.GET.get('page')
                ventas = paginator.get_page(page_number)

                return render(request, 'webapp/ventas/ventas.html', {'ventas': ventas})
            else:
                messages.warning(request, f"{login[4]} error")
                return redirect('webapp:inicioCrud')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('webapp:loginEmpleados')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('webapp:listarClientes')

    # REPORTES


def ventasjuegos(request):
    labels = []
    data = []

    juegos = Juego.objects.order_by('precio')[:5]
    for juego in juegos:
        labels.append(juego.titulo)
        data.append(juego.precio)

    return render(request, 'webapp/graficos/venta_juegos.html', {
        'labels': labels,
        'data': data,
    })


def cantidadVentas(request):
    labels = []
    data = []

    juegos = Venta_detalle.objects.order_by('id_juego')
    for juego in juegos:

        labels.append(juego.id_juego.titulo)
        data.append(juego.cantidad)

    return render(request, 'webapp/graficos/venta_juegos.html', {
        'labels': labels,
        'data': data,
    })
