# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('libro/<int:id>/', views.detalle_libro, name='detalle_libro'),
    path('libro/crear/', views.crear_libro, name='crear_libro'),
    path('libro/<int:id>/editar/', views.actualizar_libro, name='actualizar_libro'),
    path('libro/<int:id>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
    path('signup/', views.signup, name='signup'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('pago/<int:libro_id>/', views.realizar_pago, name='realizar_pago'),
    path('transaccion_exitosa/', views.transaccion_exitosa, name='transaccion_exitosa'),
]
