from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    telefono = models.IntegerField(null=True)

class Compra(models.Model):
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)

class Genero(models.Model):
    nombre = models.CharField(max_length=30)

class Juego(models.Model):
    titulo = models.CharField(max_length=100)
    fecha_lanzamiento = models.DateField()
    desarrollador = models.CharField(max_length=50)
    editor = models.CharField(max_length=50, null=True)
    descripcion = models.TextField()
    ESRB_CHOISES = (('E', 'Everyone'), ('E10', 'Everyone 10+'), ('T', 'Teen'), ('M', 'Mature 17+'), ('AO', 'Adults Only 18+'), ('RP', 'Rating Pending'))
    esrb = models.CharField(max_length=30, choices=ESRB_CHOISES, default='RP')
    stock = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    imagen = models.URLField(null=True, blank=True)
    habilitado = models.BooleanField()
    generos = models.ManyToManyField(Genero)

class Compra_detalle(models.Model):
    id_compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING)
    id_juego = models.ForeignKey(Juego, on_delete=models.DO_NOTHING)
    cantidad = models.PositiveIntegerField()

class Permiso(models.Model):
    nombre = models.CharField(max_length=20)

class Rol(models.Model):
    nombre = models.CharField(max_length=20)
    permisos = models.ManyToManyField(Permiso)

class Usuario(models.Model):
    email = models.EmailField(max_length=100)
    clave = models.CharField(50)
    id_permiso = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)

class Empleado(models.Model):
    cedula = models.IntegerField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.IntegerField()
    fecha_nacimiento = models.DateField()
    municipio_residencia = models.CharField(max_length=30)
    direccion_residencia = models.TextField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

class Venta_detalle(models.Model):
    id_producto = models.ForeignKey(Juego, on_delete=models.DO_NOTHING)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    id_venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)