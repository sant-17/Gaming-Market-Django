class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        
        if not carrito:
            self.session["carrito"] ={}
            self.carrito = self.session["carrito"]
        else:
            self.carrito= carrito
            
    def agregar(self, juego):
        """Agrega elementos al diccionario

        Args:
            juego (_type_): _description_
        """
        
        jId = str(juego.id)
        
        if jId not in self.carrito.keys():
            self.carrito[jId]={
                "juegoId" : juego.id,
                "titulo" : juego.titulo,
                "precio" : juego.precio,
                "cantidad" : 1,
                "stock":juego.stock -1,
                
            }
        else:
            if self.carrito[jId]["stock"] >= self.carrito[jId]["cantidad"] :
                self.carrito[jId]["cantidad"] +=1
                self.carrito[jId]["precio"] += juego.precio
                self.carrito[jId]["stock"] -=1
        self.guardarCarrito()
        
    def guardarCarrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
        
    def eliminar(self, juego):
        
        id = str(juego.id)        
        if id in self.carrito:
            del self.carrito[id]
            
        self.guardarCarrito()
            
    def restar(self, juego):
        
        id = str(juego.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -=1
            self.carrito[id]["stock"] +=1
            self.carrito[id]["precio"]-= juego.precio
            
            if self.carrito[id]["cantidad"] <=0: 
                self.eliminar(juego)
        self.guardarCarrito()    
        
    def stocks(self, juego):
        """verifica disponibilidad

        Args:
            juego (Juego): objeto de clase Juego

        Returns:
            bool: si no hay stock
        """
        id = str(juego.id)
        if self.carrito[id]["stock"] == 0:
            return True
    
    def limpiar (self):
        self.session["carrito"] ={}
        self.session.modified = True
        
        
