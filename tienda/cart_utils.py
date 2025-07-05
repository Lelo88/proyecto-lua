from .models import Carrito, ItemCarrito, Producto, Orden, DetalleOrden
from django.db import transaction

def obtener_carrito_activo(usuario):
    carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
    return carrito

def agregar_producto_al_carrito(usuario, producto_id, cantidad):
    producto = Producto.objects.get(id=producto_id)
    carrito = obtener_carrito_activo(usuario)

    if cantidad > producto.stock:
        raise ValueError("No hay suficiente stock disponible.")

    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)

    item.cantidad += cantidad
    if item.cantidad > producto.stock:
        raise ValueError("La cantidad excede el stock disponible.")
    
    item.save()
    return item

def quitar_producto_del_carrito(usuario, producto_id):
    carrito = obtener_carrito_activo(usuario)
    ItemCarrito.objects.filter(carrito=carrito, producto_id=producto_id).delete()

def obtener_items_del_carrito(usuario):
    carrito = obtener_carrito_activo(usuario)
    return carrito.items.select_related('producto')

@transaction.atomic
def confirmar_orden(usuario, metodo_pago=None):
    carrito = obtener_carrito_activo(usuario)
    items = carrito.items.select_related('producto')

    if not items.exists():
        raise ValueError("El carrito está vacío.")

    total = sum(item.producto.precio * item.cantidad for item in items)

    orden = Orden.objects.create(usuario=usuario, total=total, metodo_pago=metodo_pago)

    for item in items:
        DetalleOrden.objects.create(
            orden=orden,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
        item.producto.stock -= item.cantidad
        item.producto.save()

    items.delete()  # Vaciar carrito
    return orden
