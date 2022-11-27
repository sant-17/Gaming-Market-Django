from .models import *

class carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session["carrito"]
        
        if not carrito:
            self.session["carrito"] ={}
            self.carrito = self.session["carrito"]
        else:
            self.carrito= carrito
            
    def agregar(self, id):
        juego = Juego.objects.get(id = id)
        jId = str(juego.id)
        
        if jId not in self.carrito.keys():
            self.carrito[jId]={
                "juegoId" : juego.id,
                "titulo" : juego.titulo,
                "precio" : juego.precio,
                "cantidad" : 1,
            }
        else:
            self.carrito[jId]["cantidad"] +=1
            self.carrito[jId]["precio"] += juego.precio
            
            
        self.guardarCarrito()
        
    def guargarCarrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
        
    def eliminar(self,id):
        juego = Juego.objects.get(id = id)
        id = str(juego.id)
        
        if id in self.carrito:
            del self.carrito[id]
            
            self.guargarCarrito()
            
    def restar(self, id):
        juego = Juego.objects.get(id = id)
        id = str(juego.id)
        if id in self.carrito.keys():
            self.carrito[id]["catidad"] -=1
            self.carrito[id]["precio"]-= juego.precio
            
            if self.carrito[id]["cantidad"] <=0: 
                self.eliminar(id)
        self.guargarCarrito()    
        
    
    def limpiar (self):
        self.session["carrito"] ={}
        self.session.modified = True
        
        
