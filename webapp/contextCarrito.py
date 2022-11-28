def totalCarrito(request):
    total = 0
    
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            
            for key, value in request.session["carrito"].items():
               total += float(value["precio"])
                
    return {"totalCarrito": total}
        
    
    