from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, MetodoPago
from .cart_utils import agregar_producto_al_carrito, obtener_items_del_carrito, confirmar_orden
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def inicio(request):
    return render(request, 'tienda/inicio.html')

@login_required
def vista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/productos.html', {'productos': productos})

@login_required
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        try:
            agregar_producto_al_carrito(request.user, producto_id, cantidad)
            messages.success(request, "Producto agregado al carrito.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return redirect('productos')

@login_required
def ver_carrito(request):
    items = obtener_items_del_carrito(request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)
    return render(request, 'tienda/carrito.html', {'items': items, 'total': total})

@login_required
def confirmar_carrito(request):
    if request.method == 'POST':
        metodo_pago = MetodoPago.objects.first()
        try:
            orden = confirmar_orden(request.user, metodo_pago)
            messages.success(request, f"Compra realizada. Orden #{orden.id}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return redirect('carrito')
