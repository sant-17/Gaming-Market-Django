def totalCarrito(request):
    total =0
    cliente = request.session.get('logueoCliente', False)
    if cliente:
        if request.session["carrito"]:
            for key, value in request.session["carrito"].items():
                total = float(value["precio"])
                
    return {"totalCarrito": total}
        
    
    