from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Pedido, Producto, Cliente
from .forms import BusquedaForm, ProductoForm, ClienteForm, PedidoForm
from django.core.exceptions import ObjectDoesNotExist

def inicio(request):
    return render(request, 'AppCarrito/index.html')

def busqueda_productos(request):
    form = BusquedaForm()

    if request.method == 'GET':
        form = BusquedaForm(request.GET)
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            if nombre is not None:
                productos = Producto.objects.filter(nombre__icontains=nombre)
                return render(request, 'AppCarrito/busqueda_producto.html', {'productos': productos})
            else:
                return render(request, 'AppCarrito/busqueda_producto.html', {'form': form})

    return render(request, 'AppCarrito/busqueda_producto.html', {'form': form})

def mostrar_carrito(request):
    productos = request.session.get('carrito', {})
    total = sum([producto['precio'] * producto['cantidad'] for producto in productos.values()])
    return render(request, 'AppCarrito/mostrar_carrito.html', {'productos': productos, 'total': total})

@require_POST
def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    cantidad = int(request.POST.get('cantidad', 0))

    if producto_id in carrito:
        carrito[producto_id] += cantidad
    else:
        carrito[producto_id] = cantidad

    request.session['carrito'] = carrito
    return redirect('AppCarrito/mostrar_carrito')

def obtener_cliente(request):
    nombre = request.user
    cliente = Cliente.objects.get(nombre=nombre)
    return cliente


def procesar_pedidos(request):
    carrito = request.session.get('carrito', {})
    total = sum([producto['precio'] * producto['cantidad'] for producto in carrito.values()])

    try:
        cliente = obtener_cliente(request)
    except ObjectDoesNotExist:
        # Manejar el caso en el que no se encuentre ningún cliente
        # Puedes elegir entre crear un nuevo cliente o mostrar un mensaje de error
        # Aquí simplemente redireccionamos al inicio
        return redirect('inicio')

    nuevo_pedido = Pedido(total=total, cliente=cliente)
    nuevo_pedido.save()

    for producto_id, producto in carrito.items():
        nuevo_pedido.productos.create(
            producto_id=producto_id,
            cantidad=producto['cantidad']
        )

    request.session['carrito'] = {}

    return render(request, 'AppCarrito/procesar_pedidos.html')

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
           
            return redirect('mostrar_carrito')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
        
            return redirect('AppCarrito/mostrar_carrito')
    else:
        form = ClienteForm()
    return render(request, 'agregar_cliente.html', {'form': form})

def realizar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
        
            return redirect('AppCarrito/mostrar_carrito')
    else:
        form = PedidoForm()
    return render(request, 'realizar_pedido.html', {'form': form})