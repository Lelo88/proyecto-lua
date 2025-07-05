from django.contrib import admin
from .models import (
    Usuario, Categoria, Producto, MetodoPago,
    Carrito, ItemCarrito, Orden, DetalleOrden
)

# Personalización del modelo Producto (opcional pero útil)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria', 'destacado')
    list_filter = ('categoria', 'destacado')
    search_fields = ('nombre',)

# Registrar los demás modelos
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(MetodoPago)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Orden)
admin.site.register(DetalleOrden)
