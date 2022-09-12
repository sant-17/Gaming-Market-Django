from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    telefono = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.nombre}"


class Genero(models.Model):
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return f"{self.nombre}"

class Juego(models.Model):
    titulo = models.CharField(max_length=100)
    fecha_lanzamiento = models.DateField()
    desarrollador = models.CharField(max_length=50)
    editor = models.CharField(max_length=50, null=True)
    descripcion = models.TextField()
    ESRB_CHOISES = (('E', 'Everyone'), ('E10', 'Everyone 10+'), ('T', 'Teen'), ('M', 'Mature 17+'), ('AO', 'Adults Only 18+'), ('RP', 'Rating Pending'))
    esrb = models.CharField(max_length=30, choices=ESRB_CHOISES, default='RP')
    multijugador = models.BooleanField(default=False)
    stock = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    imagen = models.URLField(null=True, blank=True)
    habilitado = models.BooleanField(default=False)
    generos = models.ManyToManyField(Genero)

    def __str__(self) -> str:
        return f"{self.titulo}"

class Compra(models.Model):
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.fecha} - {self.valor}"

class Compra_detalle(models.Model):
    id_compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING)
    id_juego = models.ForeignKey(Juego, on_delete=models.DO_NOTHING)
    cantidad = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.id_compra} - {self.id_juego.titulo}"

class Permiso(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.nombre}"

class Rol(models.Model):
    nombre = models.CharField(max_length=20)
    permisos = models.ManyToManyField(Permiso)

    def __str__(self) -> str:
        return f"{self.nombre}"

class Usuario(models.Model):
    email = models.EmailField(max_length=100)
    clave = models.CharField(max_length=50)
    id_rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.email}"

class Empleado(models.Model):
    cedula = models.IntegerField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.IntegerField()
    fecha_nacimiento = models.DateField()
    municipio_residencia = models.CharField(max_length=30)
    direccion_residencia = models.TextField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.cedula} - {self.nombre}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return f"{self.fecha} - {self.id_cliente.nombre} {self.id_cliente.apellido}"

class Venta_detalle(models.Model):
    id_juego = models.ForeignKey(Juego, on_delete=models.DO_NOTHING)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    id_venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.id_juego.titulo} - {self.cantidad}"