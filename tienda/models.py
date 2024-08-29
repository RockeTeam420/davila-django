from django.contrib.auth.models import AbstractUser
from .authentication import CustomUserManager
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings
# Create your models here.

class Usuario(AbstractUser):
	username = None
	nombre = models.CharField(max_length=254)
	email = models.EmailField(max_length=254, unique=True)
	password = models.CharField(max_length=254)
	ROLES = (
		(1, "Administrador"),
		(2, "Despachador"),
		(3, "Cliente"),
		(4, "Domiciliario")
	)
	rol = models.IntegerField(choices=ROLES, default=3)
	foto = models.ImageField(upload_to="fotos/", default="fotos/default.png", blank=True)
	token_recuperar = models.CharField(max_length=254, default="", blank=True, null=True)
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["nombre"]
	objects = CustomUserManager()

	def __str__(self):
		return self.nombre

class Categoria(models.Model):
	nombre = models.CharField(max_length=254)
	descripcion = models.TextField()

	def __str__(self):
		return self.nombre


class CategoriaEtiqueta(models.Model):
	nombre = models.CharField(max_length=254, unique=True)

	def __str__(self):
		return self.nombre
	
class SubCategoriaEtiqueta(models.Model):
	nombre = models.CharField(max_length=254)
	id_categoria_etiqueta = models.ForeignKey(CategoriaEtiqueta, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre
	

class Producto(models.Model):
	nombre = models.CharField(max_length=254)
	informacion = models.CharField(max_length=254)
	precio = models.IntegerField()
	inventario = models.IntegerField()
	fecha_creacion = models.DateField()
	categoria = models.ForeignKey(CategoriaEtiqueta,on_delete=models.CASCADE)
	foto = models.ImageField(upload_to="fotos_productos/", default="fotos_productos/default.png")

	def __str__(self):
		return self.nombre

class Tallas(models.Model):    
	talla = models.CharField(max_length=254)
 
	def __str__(self):
    		return self.talla
   
class ProductoTallas(models.Model):
	id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	id_talla = models.ForeignKey(Tallas, on_delete=models.CASCADE)
 
	def __str__(self):
    		return self.nombre

class ProductoSubCategoria(models.Model):
	id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	id_sub_categoria_etiqueta = models.ForeignKey(SubCategoriaEtiqueta, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.id_producto}, {self.id_sub_categoria_etiqueta}'

class Venta(models.Model):
	fecha_venta = models.DateTimeField(auto_now=True)
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	ESTADOS = (
		(1, 'Pendiente'),
		(2, 'Pagada'),
		(3, 'Rechazada'),
	)
	estado = models.IntegerField(choices=ESTADOS, default=1)

	def __str__(self):
		return f"{self.id} - {self.usuario}"


class DetalleVenta(models.Model):
	venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	cantidad = models.IntegerField()
	precio_historico = models.IntegerField()

	def __str__(self):
		return f"{self.id} - {self.venta}"



class Pedido(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    direccion = models.TextField()
    contacto = models.IntegerField()
    TIPO_PAGO = (
		(1, "Tarjeta de credito"),
		(2, "Tarjeta debito"),
		(3, "Efectivo")
	)
    tipo_pago = models.IntegerField(choices=TIPO_PAGO)
    
    def __str__(self):
    		return f"{self.tipo_pago}"
    
class Devoluciones(models.Model):
    nombre = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True)
    telefono = models.IntegerField()
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre
    
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)