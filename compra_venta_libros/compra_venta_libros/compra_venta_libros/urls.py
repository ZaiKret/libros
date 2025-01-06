# compra_venta_libros/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),  # Incluye las rutas de libros aquí
    path('accounts/', include('django.contrib.auth.urls')),  # Rutas de autenticación
]
