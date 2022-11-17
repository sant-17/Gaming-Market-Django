from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Genero)
admin.site.register(Juego)
admin.site.register(Usuario)
admin.site.register(Venta)
admin.site.register(Venta_detalle)