from django.shortcuts import render, get_object_or_404, redirect
from .models import Libro, Transaccion
from .forms import LibroForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import stripe

stripe.api_key = "12345"

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Listar libros
def lista_libros(request):
    categoria = request.GET.get('categoria', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')

    libros = Libro.objects.all()

    if categoria:
        libros = libros.filter(categoria__icontains=categoria)
    if precio_min:
        libros = libros.filter(precio__gte=precio_min)
    if precio_max:
        libros = libros.filter(precio__lte=precio_max)

    return render(request, 'lista_libros.html', {'libros': libros})

# Detalle del libro
def detalle_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    return render(request, 'detalle_libro.html', {'libro': libro})

# Crear libro sin autenticación
from django.contrib.auth.decorators import login_required

@login_required
def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.usuario = request.user  # Aquí se asigna el usuario autenticado
            libro.save()
            return redirect('lista_libros')
    else:
        form = LibroForm()
    return render(request, 'crear_libro.html', {'form': form})


@login_required
def actualizar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if libro.usuario != request.user:
        return redirect('lista_libros')

    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'actualizar_libro.html', {'form': form})

@login_required
def eliminar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if libro.usuario != request.user:
        return redirect('lista_libros')

    if request.method == 'POST':
        libro.delete()
        return redirect('lista_libros')
    return render(request, 'eliminar_libro.html', {'libro': libro})

def realizar_pago(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    # Convertir el precio a centavos (multiplicando por 100)
    precio_centavos = int(libro.precio * 100)  # Stripe requiere el monto en centavos

    if request.method == 'POST':
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=precio_centavos,  # Monto en centavos
                currency='usd',
                description=f"Compra de {libro.titulo}",
                source=token
            )

            if charge.status == 'succeeded':
                # Procesar la transacción y redirigir al usuario a la página de éxito
                return redirect('transaccion_exitosa')

        except stripe.error.StripeError as e:
            return render(request, 'error_pago.html', {'error': e})

    return render(request, 'pago_libro.html', {'libro': libro})

@login_required
def perfil_usuario(request):
    usuario = request.user
    libros_vendidos = Libro.objects.filter(usuario=usuario)
    compras = Transaccion.objects.filter(comprador=usuario)
    return render(request, 'perfil_usuario.html', {'usuario': usuario, 'libros_vendidos': libros_vendidos, 'compras': compras})


def transaccion_exitosa(request):
    return render(request, 'transaccion_exitosa.html')