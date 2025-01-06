from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User

    def __str__(self):
        return self.titulo


class Transaccion(models.Model):
    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compras")
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ventas")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Valor por defecto de 0 para monto
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comprador} compró {self.libro} por {self.monto}"
