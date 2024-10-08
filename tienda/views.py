from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db import IntegrityError, transaction
from rest_framework import viewsets 
from .serializers import *
# Para tomar el from desde el settings
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
import re
from .crypt import *
from .forms import ImageUploadForm
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save

# Importamos todos los modelos de la base de datos
from .models import *

# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class DevolucionesViewSet(viewsets.ModelViewSet):
    queryset = Devoluciones.objects.all()
    serializer_class = DevolucionesSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
""" class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    """
    
class CategoriaEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = CategoriaEtiqueta.objects.all()
    serializer_class = CategoriaEtiquetaSerializer

class SubCategoriaEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = SubCategoriaEtiqueta.objects.all()
    serializer_class = SubCategoriaEtiquetaSerializer
    
class ProductoSubCategoriaViewSet(viewsets.ModelViewSet):
    queryset = ProductoSubCategoria.objects.all()
    serializer_class = ProductoSubCategoriaSerializer
    
class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    
class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    
def index(request):
	logueo = request.session.get("logueo", False)

	if logueo == False:
		return render(request, "tienda/login/login.html")
	else:
		return redirect("inicio")
	
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CategoriaViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer


class UsuarioViewSet(viewsets.ModelViewSet):	
	authentication_classes = [TokenAuthentication]
	#permission_classes = [IsAuthenticated]
	queryset = Usuario.objects.all()
	serializer_class = UsuarioSerializer

def registro(request):
    return render(request,"tienda/login/registro.html")


def registrar_usuario(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		user = request.POST.get("correo")
		clave1 = request.POST.get("clave1")
		clave2 = request.POST.get("clave2")
		switch = request.POST.get("switchTyC")
		if switch:
			if not nombre or not user:
				messages.warning(request,"Campos vacios, ingrese datos!!")
				return redirect("inicio")
			if not re.match(r"^[a-zA-Z\s]+$", nombre):
				messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
			if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user):
				messages.error(request, f"El correo ingresado no es valido")
			if clave1 == clave2:
				q = Usuario(
				nombre=nombre,
				email=user,
				password=hash_password(clave1)
				)
				q.save()
				messages.success(request, "Usuario registrado correctamente!!")
				return redirect("inicio")
			else:
				messages.warning(request, "No concuerdan las contraseñas")
				return redirect("inicio")
		else:
			messages.error(request, "Debe aceptar los terminos y condiciones")
			return redirect("inicio")
	else:
		return redirect("inicio")
#-------------------

def usuarios(request):
	q = Usuario.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/usuarios/usuarios.html", contexto)



def usuarios_form(request):
	return render(request, "tienda/usuarios/usuarios_form.html")


def usuarios_crear(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		email = request.POST.get("email")
		password = request.POST.get("password")
		rol = request.POST.get("rol")
		if not re.match(r"^[a-zA-Z\s]+$", nombre):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = CategoriaEtiqueta(
				nombre = nombre,
				email = email,
				password = password,
				rol = rol
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("usuarios_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("usuarios_listar")


def usuarios_eliminar(request, id):
	try:
		q = Usuario.objects.get(pk=id)
		q.delete()
		messages.success(request, "Usuario eliminado correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("usuarios_listar")


def usuarios_formulario_editar(request, id):
	q = Usuario.objects.get(pk=id)
	contexto = {"data": q}
	return render(request, "tienda/usuarios/usuarios_formulario_editar.html", contexto)

def usuarios_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nombre = request.POST.get("nombre")
		email = request.POST.get("email")
		password = request.POST.get("password")
		rol = request.POST.get("rol")

		try:
			q = Usuario.objects.get(pk=id)
			q.nombre = nombre
			q.email = email
			q.password = password
			q.rol = rol
			q.save()
			messages.success(request, "Usuario actualizado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("usuarios_listar")
#---------------

def login(request):
	if request.method == "POST":
		user = request.POST.get("email")
		passw = request.POST.get("password")
		switch = request.POST.get("switchTyC")
		# select * from Usuario where correo = "user" and clave = "passw"
		if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user):
			messages.error(request, f"El correo ingresado no es valido")
		if switch:
			try:
				q = Usuario.objects.get(email=user)
				if verify_password(passw, q.password):
				# Crear variable de sesión
					request.session["logueo"] = {
						"id": q.id,
						"nombre": q.nombre,
						"rol": q.rol,
						"nombre_rol": q.get_rol_display()
					}
					request.session["carrito"] = []
					request.session["items"] = 0
					messages.success(request, f"Bienvenido {q.nombre}!!")
				return redirect("inicio")
			except Exception as e:
				messages.error(request, f"{e} Error: Usuario o contraseña incorrectos...")
				return redirect("inicio")
		else:
			messages.error(request, "Debe aceptar los terminos y condiciones")
			return redirect('inicio')

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("inicio")


def logout(request):
	try:
		del request.session["logueo"]
		del request.session["carrito"]
		del request.session["items"]
		messages.success(request, "Sesión cerrada correctamente!")
		return redirect("inicio")
	except Exception as e:
		messages.warning(request, "No se pudo cerrar sesión...")
		return redirect("")


def inicio(request):
	logueo = request.session.get("logueo", False)
 
	productos = Producto.objects.all()
	tallas = Tallas.objects.all()
	proTallas = ProductoTallas.objects.select_related('id_talla', 'id_producto')
	etiquetas = SubCategoriaEtiqueta.objects.all()
	categorias = CategoriaEtiqueta.objects.all()
	etq_categorias=[]
	for c in categorias:
		etiquetas = SubCategoriaEtiqueta.objects.filter(id_categoria_etiqueta=c)
		etq_categorias.append(etiquetas)
	
	
     
	cat = request.GET.get("cat")
	etq = request.GET.getlist("servicios")
 
	
	if cat == None:
    		productos = Producto.objects.all()
	else:
		c = CategoriaEtiqueta.objects.get(pk=cat)
		productos = Producto.objects.filter(categoria=c)
	

	if etq == None:
    		productos = Producto.objects.all()
	

		

	contexto = {"data": productos, "cat": categorias, "etq": etq_categorias, "tallas":tallas, "proTallas":proTallas}
	return render(request, "tienda/inicio/inicio.html", contexto)
	
def recuperar_clave(request):
	if request.method == "POST":
		email = request.POST.get("correo")
		try:
			q = Usuario.objects.get(email=email)
			from random import randint
			import base64
			token = base64.b64encode(str(randint(100000, 999999)).encode("ascii")).decode("ascii")
			print(token)
			q.token_recuperar = token
			q.save()
			# enviar correo de recuperación
			destinatario = email
			mensaje = f"""
					<h1 style='color:blue;'>Tienda virtual</h1>
					<p>Usted ha solicitado recuperar su contraseña, haga clic en el link y digite el token.</p>
					<p>Token: <strong>{token}</strong></p>
					<a href='http://127.0.0.1:8000/tienda/verificar_recuperar/?correo={email}'>Recuperar...</a>
					"""
			try:
				msg = EmailMessage("Tienda ADSO", mensaje, settings.EMAIL_HOST_USER, [destinatario])
				msg.content_subtype = "html"  # Habilitar contenido html
				msg.send()
				messages.success(request, "Correo enviado!!")
			except BadHeaderError:
				messages.error(request, "Encabezado no válido")
			except Exception as e:
				messages.error(request, f"Error: {e}")
			# fin -
		except Usuario.DoesNotExist:
			messages.error(request, "No existe el usuario....")
		return redirect("recuperar_clave")
	else:
		return render(request, "tienda/login/recuperar.html")


def verificar_recuperar(request):
	if request.method == "POST":
		if request.POST.get("check"):
			# caso en el que el token es correcto
			email = request.POST.get("correo")
			q = Usuario.objects.get(email=email)

			c1 = request.POST.get("nueva1")
			c2 = request.POST.get("nueva2")

			if c1 == c2:
				# cambiar clave en DB
				q.password = hash_password(c1)
				q.token_recuperar = ""
				q.save()
				messages.success(request, "Contraseña guardada correctamente!!")
				return redirect("index")
			else:
				messages.info(request, "Las contraseñas nuevas no coinciden...")
				return redirect("verificar_recuperar")+"/?correo="+email
		else:
			# caso en el que se hace clic en el correo-e para digitar token
			email = request.POST.get("correo")
			token = request.POST.get("token")
			q = Usuario.objects.get(email=email)
			if (q.token_recuperar == token) and q.token_recuperar != "":
				contexto = {"check": "ok", "correo":email}
				return render(request, "tienda/login/verificar_recuperar.html", contexto)
			else:
				messages.error(request, "Token incorrecto")
				return redirect("verificar_recuperar")	# falta agregar correo como parametro url
	else:
		correo = request.GET.get("correo")
		contexto = {"correo":correo}
		return render(request, "tienda/login/verificar_recuperar.html", contexto)


from .decorador_especial import *






@login_requerido
def categorias(request):
	q = CategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias.html", contexto)



def categorias_form(request):
	return render(request, "tienda/categorias/categorias_form.html")


def categorias_crear(request):
	if request.method == "POST":
		nomb = request.POST.get("nombre")
		if not re.match(r"^[a-zA-Z\s]+$", nomb):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = CategoriaEtiqueta(
				nombre=nomb,
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("categorias_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("categorias_listar")


def categorias_eliminar(request, id):
	try:
		q = CategoriaEtiqueta.objects.get(pk=id)
		q.delete()
		messages.success(request, "Categoría eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("categorias_listar")


def categorias_formulario_editar(request, id):
	q = CategoriaEtiqueta.objects.get(pk=id)
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias_formulario_editar.html", contexto)

def categorias_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")

		try:
			q = CategoriaEtiqueta.objects.get(pk=id)
			q.nombre = nomb
			q.descripcion = desc
			q.save()
			messages.success(request, "Categoría actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("categorias_listar")


@login_requerido
def productos(request):
    q = Producto.objects.all()
    proTallas = ProductoTallas.objects.select_related('id_talla', 'id_producto')
    
    productos = []
    
    for i in q:
        producto = {
            'nombre': i.nombre,
            'id': i.id,
            'etiqueta': [],
            'precio': i.precio,
            'inventario': i.inventario,
            'fecha_creacion': i.fecha_creacion,
            'categoria': i.categoria,
            'tallas': []
        }

        x = ProductoSubCategoria.objects.all()
        for y in x:
            if i.id == y.id_producto.id:
                tag = SubCategoriaEtiqueta.objects.get(pk=y.id_sub_categoria_etiqueta.id)
                producto["etiqueta"].append(tag)

        for pt in proTallas:
            if pt.id_producto.id == i.id:
                producto['tallas'].append(pt.id_talla.talla)

        productos.append(producto)

    contexto = { 
        "data": productos
    }

    return render(request, "tienda/productos/productos.html", contexto)



def productos_form(request):
	q = CategoriaEtiqueta.objects.all()
	e = SubCategoriaEtiqueta.objects.all()
	t = Tallas.objects.all()
	contexto = {"data": q, "etiqueta": e, "talla":t}
	return render(request, "tienda/productos/productos_form.html", contexto)


def productos_crear(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		precio = request.POST.get("precio")
		inventario = request.POST.get("inventario")
		fecha_creacion = request.POST.get("fecha_creacion")
		categoria = CategoriaEtiqueta.objects.get(pk=request.POST.get("categoria"))
		etiquetas = request.POST.getlist("etiqueta")
		tallas = request.POST.getlist("talla")
		foto = request.FILES["foto"]

		if not re.match(r"^\d", precio):
    			messages.error(request, f"El precio solo puede llevar valores numericos")
		if not re.match(r"^\d", inventario):
    			messages.error(request, f"El inventario solo puede llevar valores numericos")
		try:
			q = Producto(
				nombre=nombre,
				precio=precio,
				inventario=inventario,
				fecha_creacion=fecha_creacion,
				categoria=categoria,
				foto=foto
			)
			q.save()

			for etiqueta_id in etiquetas:
				etiqueta = SubCategoriaEtiqueta.objects.get(pk=etiqueta_id)
				
				ProductoSubCategoria.objects.create(
					id_producto = q,
					id_sub_categoria_etiqueta = etiqueta
				)

			for talla_id in tallas:
				talla = Tallas.objects.get(pk=talla_id)
				ProductoTallas.objects.create(
					id_producto = q,
					id_talla = talla
				)
   
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: No se enviaron datos...{e}")
		return redirect("productos_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("productos_listar")


def productos_eliminar(request, id):
	try:
		q = Producto.objects.get(pk=id)
		q.delete()
		messages.success(request, "Producto eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("productos_listar")


def productos_formulario_editar(request, id):
	q = Producto.objects.get(pk=id)
	c = CategoriaEtiqueta.objects.all()
	e = SubCategoriaEtiqueta.objects.all()
	t = Tallas.objects.all()
	pt = ProductoTallas.objects.all()
	contexto = {"data": q, "categoria": c, "etiqueta":e, "talla":t, "proTallas":pt}
	return render(request, "tienda/productos/productos_formulario_editar.html", contexto)

def productos_actualizar(request):
    if request.method == "POST":
        id_producto = request.POST.get("id")
        nombre = request.POST.get("nombre")
        precio = request.POST.get("precio")
        inventario = request.POST.get("inventario")
        fecha_creacion = request.POST.get("fecha_creacion")
        categoria_id = request.POST.get("categoria")
        etiquetas_ids = request.POST.getlist("etiqueta")
        tallas = request.POST.getlist("tallas")

        # Validación básica de los campos de precio e inventario
        if not precio.isdigit():
            messages.error(request, "El precio solo puede llevar valores numéricos")
            return redirect("productos_listar")

        if not inventario.isdigit():
            messages.error(request, "El inventario solo puede llevar valores numéricos")
            return redirect("productos_listar")

        try:
            # Obtener el producto a actualizar
            producto = Producto.objects.get(pk=id_producto)

            # Actualizar los campos del producto
            producto.nombre = nombre
            producto.precio = precio
            producto.inventario = inventario
            producto.fecha_creacion = fecha_creacion
            producto.categoria_id = categoria_id

            # Guardar el producto actualizado
            producto.save()

            # Limpiar y actualizar las etiquetas asociadas al producto
            ProductoSubCategoria.objects.filter(id_producto=producto).delete()  # Limpiar etiquetas existentes

            for etiqueta_id in etiquetas_ids:
                etiqueta = SubCategoriaEtiqueta.objects.get(pk=etiqueta_id)
                ProductoSubCategoria.objects.create(
					id_producto = producto,
					id_sub_categoria_etiqueta = etiqueta
				)

            messages.success(request, "Producto actualizado correctamente")
        except Producto.DoesNotExist:
            messages.error(request, "El producto especificado no existe")
        except SubCategoriaEtiqueta.DoesNotExist:
            messages.error(request, "Una de las etiquetas especificadas no existe")
        except Exception as e:
            messages.error(request, f"Error al actualizar el producto: {e}")

    else:
        messages.warning(request, "Error: No se enviaron datos")

    return redirect("productos_listar")


def ver_perfil(request):
	logueo = request.session.get("logueo", False)
	# Consultamos en DB por el ID del usuario logueado....
	q = Usuario.objects.get(pk=logueo["id"])
	contexto = {"data": q}
	return render(request, "tienda/login/perfil.html", contexto)


def cambio_clave_formulario(request):
	return render(request, "tienda/login/cambio_clave.html")


def cambiar_clave(request):
    if request.method == "POST":
        logueo = request.session.get("logueo", False)
        try:
            q = Usuario.objects.get(pk=logueo["id"])
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado...")
            return redirect('cc_formulario')

        c1 = request.POST.get("nueva1")
        c2 = request.POST.get("nueva2")

        if q.check_password(request.POST.get("clave")):
            if c1 == c2:
                q.set_password(c1)
                q.save()
                messages.success(request, "Contraseña guardada correctamente!!")
            else:
                messages.info(request, "Las contraseñas nuevas no coinciden...")
        else:
            messages.error(request, "Contraseña no válida...")
    else:
        messages.warning(request, "Error: No se enviaron datos...")

    return redirect('cc_formulario')


def carrito_add(request):
	if request.method == "POST":
		try:
			carrito = request.session.get("carrito", False)
			if not carrito:
				request.session["carrito"] = []
				request.session["items"] = 0
				carrito = []

			id_producto = int(request.POST.get("id"))
			cantidad = request.POST.get("cantidad")
			# Consulto el producto en DB...........................
			q = Producto.objects.get(pk=id_producto)
			for p in carrito:
				if p["id"] == id_producto:
					if q.inventario >= (p["cantidad"] + int(cantidad)) and int(cantidad) > 0:
						p["cantidad"] += int(cantidad)
						p["subtotal"] = p["cantidad"] * q.precio
					else:
						print("Cantidad supera inventario...")
						messages.warning(request, "Cantidad supera inventario...")
					break
			else:
				print("No existe en carrito... lo agregamos")
				if q.inventario >= int(cantidad) and int(cantidad) > 0:
					carrito.append(
						{
							"id": q.id,
							"foto": q.foto.url,
							"producto": q.nombre,
							"precio": q.precio,
							"cantidad": int(cantidad),
							"subtotal": int(cantidad) * q.precio
						}
					)
				else:
					print("Cantidad supera inventario...")
					messages.warning(request, "No se puede agregar, no hay suficiente inventario.")

			# Actualizamos variable de sesión carrito...
			request.session["carrito"] = carrito

			contexto = {
				"items": len(carrito),
				"total": sum(p["subtotal"] for p in carrito)
			}
			request.session["items"] = len(carrito)

			return render(request, "tienda/carrito/carrito.html", contexto)
		except ValueError as e:
			messages.error(request, f"Error: Digite un valor correcto para cantidad")
			return HttpResponse("Error")
		except Exception as e:
			messages.error(request, f"Ocurrió un Error: {e}")
			return HttpResponse("Error")
	else:
		messages.warning(request, "No se enviaron datos.")
		return HttpResponse("Error")


def carrito_ver(request):
	carrito = request.session.get("carrito", False)
	if not carrito:
		request.session["carrito"] = []
		request.session["items"] = 0
		contexto = {
			"items": 0,
			"total": 0
		}
	else:
		contexto = {
			"items": len(carrito),
			"total": sum(p["subtotal"] for p in carrito)
		}
		request.session["items"] = len(carrito)

	return render(request, "tienda/carrito/carrito.html", contexto)


def vaciar_carrito(request):
	request.session["carrito"] = []
	request.session["items"] = 0
	return redirect("inicio")


def eliminar_item_carrito(request, id_producto):
	try:
		carrito = request.session.get("carrito", False)
		if carrito != False:
			for i, item in enumerate(carrito):
				if item["id"] == id_producto:
					carrito.pop(i)
					break
			else:
				messages.warning(request, "No se encontró el ítem en el carrito.")

		request.session["items"] = len(carrito)
		request.session["carrito"] = carrito
		return redirect("carrito_ver")
	except:
		return HttpResponse("Error")


def actualizar_totales_carrito(request, id_producto):
	carrito = request.session.get("carrito", False)
	cantidad = request.GET.get("cantidad")

	if carrito != False:
		for i, item in enumerate(carrito):
			if item["id"] == id_producto:
				q = Producto.objects.get(pk=id_producto)
				if q.inventario >= int(cantidad) and int(cantidad) > 0:
					item["cantidad"] = int(cantidad)
					item["subtotal"] = int(cantidad) * item["precio"]
					break
				else:
					print("Cantidad supera inventario...")
					messages.warning(request, "No se puede agregar, no hay suficiente inventario.")
					return HttpResponse("Error")
		else:
			messages.warning(request, "No se encontró el ítem en el carrito.")

	request.session["items"] = len(carrito)
	request.session["carrito"] = carrito
	return redirect("carrito_ver")


def realizar_venta(request):
    try:
        logueo = request.session.get("logueo")
        usuario = Usuario.objects.get(pk=logueo["id"])
        nueva_venta = Venta.objects.create(usuario=usuario)

        carrito = request.session.get("carrito", [])
        for item in carrito:
            producto = Producto.objects.get(pk=item["id"])
            cantidad = item["cantidad"]

            detalle_venta = DetalleVenta.objects.create(
                venta=nueva_venta,
                producto=producto,
                cantidad=cantidad,
                precio_historico=producto.precio
            )

            producto.inventario -= cantidad
            producto.save()

        request.session["carrito"] = []
        request.session["items"] = 0

        messages.success(request, "¡La compra se realizó con éxito!")

    except Producto.DoesNotExist as e:
        messages.error(request, f"Error al procesar la compra: {e}")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al procesar la compra: {e}")

    return redirect("inicio")

def ventas_ver(request):
    try:
        ventas = Venta.objects.all()
        ventas_con_detalles = []
        
        if request.method == "POST":
            id_producto = int(request.POST.get("id"))
            cantidad = int(request.POST.get("cantidad", 0))
            
            if cantidad <= 0:
                raise ValueError("Cantidad debe ser mayor que 0")

            producto = Producto.objects.get(id=id_producto)
            
            for venta in ventas:
                detalles = DetalleVenta.objects.filter(venta=venta)
                for detalle in detalles:
                    if detalle.producto.id == id_producto:
                        if producto.inventario >= (detalle.cantidad + cantidad):
                            detalle.cantidad += cantidad
                            detalle.subtotal = detalle.cantidad * detalle.precio_historico
                            detalle.save()
                        break
                ventas_con_detalles.append({
                    'venta': venta,
                    'detalles': detalles
                })
        
        else:
            for venta in ventas:
                detalles = DetalleVenta.objects.filter(venta=venta)
                ventas_con_detalles.append({
                    'venta': venta,
                    'detalles': detalles
                })
        
        contexto = {
            'ventas_con_detalles': ventas_con_detalles
        }
        
        return render(request, "tienda/ventas/ventas_ver.html", contexto)
    
    except Exception as e:
        messages.error(request, f"Ocurrió un error al recuperar las ventas: {e}")
        return render(request, "tienda/ventas/ventas_ver.html", {'ventas_con_detalles': []})

@transaction.atomic
def guardar_venta(request):
	carrito = request.session.get("carrito", False)
	logueo = request.session.get("logueo", False)
	try:
		r = Venta(usuario=Usuario.objects.get(pk=logueo["id"]))
		r.save()

		for i, p in enumerate(carrito):
			try:
				pro = Producto.objects.get(pk=p["id"])
				print(f"ok producto {p['producto']}")
			except Producto.DoesNotExist:
				# elimino el producto no existente del carrito...
				carrito.pop(i)
				request.session["carrito"] = carrito
				request.session["items"] = len(carrito)
				raise Exception(f"El producto '{p['producto']}' ya no existe")

			if int(p["cantidad"]) > pro.inventario:
				raise Exception(f"La cantidad del producto '{p['producto']}' supera el inventario")

			det = DetalleVenta(
				venta=r,
				producto=pro,
				cantidad=int(p["cantidad"]),
				precio_historico=int(p["precio"])
			)
			det.save()
		messages.success(request, "Venta realizada correctamente!!")
	except Exception as e:
		transaction.set_rollback(True)
		messages.error(request, f"Error: {e}")

	return redirect("inicio")

def realizar_pedido(request):
    try:
        logueo = request.session.get("logueo")
        usuario = Usuario.objects.get(pk=logueo["id"])
        nueva_venta = Venta.objects.create(usuario=usuario)

        carrito = request.session.get("carrito", [])
        for item in carrito:
            producto = Producto.objects.get(pk=item["id"])
            cantidad = item["cantidad"]

            detalle_venta = DetalleVenta.objects.create(
                venta=nueva_venta,
                producto=producto,
                cantidad=cantidad,
                precio_historico=producto.precio
            )

            producto.inventario -= cantidad
            producto.save()

        request.session["carrito"] = []
        request.session["items"] = 0

        messages.success(request, "¡La compra se realizó con éxito!")

    except Producto.DoesNotExist as e:
        messages.error(request, f"Error al procesar la compra: {e}")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al procesar la compra: {e}")

    return redirect("inicio")

def pedido_ver(request):
    try:
        ventas = Venta.objects.all()
        ventas_con_detalles = []
        
        if request.method == "POST":
            id_producto = int(request.POST.get("id"))
            cantidad = int(request.POST.get("cantidad", 0))
            
            if cantidad <= 0:
                raise ValueError("Cantidad debe ser mayor que 0")

            producto = Producto.objects.get(id=id_producto)
            
            for venta in ventas:
                detalles = DetalleVenta.objects.filter(venta=venta)
                for detalle in detalles:
                    if detalle.producto.id == id_producto:
                        if producto.inventario >= (detalle.cantidad + cantidad):
                            detalle.cantidad += cantidad
                            detalle.subtotal = detalle.cantidad * detalle.precio_historico
                            detalle.save()
                        break
                ventas_con_detalles.append({
                    'venta': venta,
                    'detalles': detalles
                })
        
        else:
            for venta in ventas:
                detalles = DetalleVenta.objects.filter(venta=venta)
                ventas_con_detalles.append({
                    'venta': venta,
                    'detalles': detalles
                })
        
        contexto = {
            'ventas_con_detalles': ventas_con_detalles
        }
        
        return render(request, "tienda/pedidos/pedido_ver.html", contexto)
    
    except Exception as e:
        messages.error(request, f"Ocurrió un error al recuperar las ventas: {e}")
        return render(request, "tienda/pedidos/pedido_ver.html", {'ventas_con_detalles': []})

def pedido_eliminar(request, id):
    try:
        venta = get_object_or_404(Venta, pk=id)
        venta.delete()
        messages.success(request, "Venta eliminada correctamente!!")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect("ventas_ver")

@transaction.atomic
def guardar_pedido(request):
	carrito = request.session.get("carrito", False)
	logueo = request.session.get("logueo", False)
	try:
		# Genero encabezado de venta, para tener ID y guardar detalle
		r = Venta(usuario=Usuario.objects.get(pk=logueo["id"]))
		r.save()

		for i, p in enumerate(carrito):
			try:
				pro = Producto.objects.get(pk=p["id"])
				print(f"ok producto {p['producto']}")
			except Producto.DoesNotExist:
				# elimino el producto no existente del carrito...
				carrito.pop(i)
				request.session["carrito"] = carrito
				request.session["items"] = len(carrito)
				raise Exception(f"El producto '{p['producto']}' ya no existe")

			if int(p["cantidad"]) > pro.inventario:
				raise Exception(f"La cantidad del producto '{p['producto']}' supera el inventario")

			det = DetalleVenta(
				venta=r,
				producto=pro,
				cantidad=int(p["cantidad"]),
				precio_historico=int(p["precio"])
			)
			det.save()
		messages.success(request, "Venta realizada correctamente!!")
	except Exception as e:
		transaction.set_rollback(True)
		messages.error(request, f"Error: {e}")

	return redirect("inicio")

def prueba_correo(request):
	destinatario = "hammer.hernandez10@gmail.com"
	mensaje = """
		<h1 style='color:blue;'>Tienda virtual</h1>
		<p>Su pedido está listo y en estado "creado".</p>
		<h1 style='color:red;'> ESTA MUY ENAMORADO </h1>
		<p>Tienda ADSO, 2024</p>
		"""
 	
	try:
		msg = EmailMessage("Tienda ADSO", mensaje, settings.EMAIL_HOST_USER, [destinatario])
		msg.content_subtype = "html"  # Habilitar contenido html
		msg.send()
		return HttpResponse("Correo enviado")
	except BadHeaderError:
		return HttpResponse("Encabezado no válido")
	except Exception as e:
		return HttpResponse(f"Error: {e}")
	




def etiquetas_listar(request):
	q = SubCategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/subcategoria/etiquetas.html", contexto)

def etiquetas_form(request):
	q = CategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/subcategoria/etiquetas_form_crear.html", contexto)

def etiquetas_crear(request):
	if request.method == "POST":
		nomb = request.POST.get("nombre")
		cat = CategoriaEtiqueta(pk=request.POST.get("categoriaEtiqueta"))
		if not re.match(r"^[a-zA-Z\s]+$", nomb):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = SubCategoriaEtiqueta(
				nombre=nomb,
				id_categoria_etiqueta=cat
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: No se enviaron los datos...")
		return redirect("etiquetas_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("etiquetas_listar")

def etiquetas_eliminar(request, id):
	try:
		q = SubCategoriaEtiqueta.objects.get(pk=id)
		q.delete()
		messages.success(request, "Etiqueta eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("etiquetas_listar")

def etiquetas_formulario_editar(request, id):
	q = SubCategoriaEtiqueta.objects.get(pk=id)
	c = CategoriaEtiqueta.objects.all()
	contexto = {"data": q, "categorias": c}
	return render(request, "tienda/categorias/subcategoria/etiquetas_form_editar.html", contexto)

def etiquetas_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		cat = CategoriaEtiqueta.objects.get(pk=request.POST.get("categoriaEtiqueta"))
		if not re.match(r"^[a-zA-Z\s]+$", nomb):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = SubCategoriaEtiqueta.objects.get(pk=id)
			q.nombre = nomb
			q.id_categoria_etiqueta = cat
			q.save()
			messages.success(request, "Etiqueta actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("etiquetas_listar")

def term_y_cond(request):
    return render(request, "tienda/term_y_cond/term_y_cond.html")



def devoluciones(request):
    q = Devoluciones.objects.all()
    estados = Devoluciones._meta.get_field('estado').choices
    print(f"Estados: {estados}")  # Para depuración
    contexto = {"data": q, "estados": estados}
    return render(request, "tienda/devoluciones/devoluciones.html", contexto)


def ver_devolucion(request):
	q = Devoluciones.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/devoluciones/ver_devolucion.html", contexto)

from django.shortcuts import get_object_or_404, redirect

def estado_devolucion(request, id):
    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        print(f"Nuevo estado recibido: {nuevo_estado}")  # Para depuración
        if nuevo_estado is None:
            messages.error(request, "No se recibió un estado válido.")
            return redirect("devoluciones")

        try:
            devolucion = Devoluciones.objects.get(pk=id)
            devolucion.estado = int(nuevo_estado)
            devolucion.save()
            messages.success(request, "Estado actualizado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el estado: {e}")
    else:
        messages.warning(request, "No se enviaron datos.")
    
    return redirect("devoluciones")

def devoluciones_form(request):
	q = CategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/devoluciones/devoluciones_form.html", contexto)

def devoluciones_crear(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        descripcion = request.POST.get("descripcion")
        image = request.FILES.get("image") 
        print(f"Datos recibidos: {nombre}, {email}, {telefono}, {descripcion}")
        
        try:
            q = Devoluciones(
                nombre=nombre,
                email=email,
                telefono=telefono,
                descripcion=descripcion,
                estado=1,
                image=image
            )
            q.save()
            messages.success(request, "Guardado correctamente!!")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("devoluciones")


def devoluciones_formulario_editar(request, id):
	q = Devoluciones.objects.get(pk=id)
	contexto = {"data": q}
	return render(request, "tienda/devoluciones/devoluciones_formulario_editar.html", contexto)

def devoluciones_actualizar(request):
    if request.method == "POST":
        id = request.POST.get("id")
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        descripcion = request.POST.get("descripcion")
        image = request.FILES.get("image")

        try:
            q = Devoluciones.objects.get(pk=id)
            q.nombre = nombre
            q.email = email
            q.telefono = telefono
            q.descripcion = descripcion
            
            if image:
                q.image = image
            
            q.save()
            messages.success(request, "Devolución actualizada correctamente!!")
        except Exception as e:
            messages.error(request, f"Error {e}")
    else:
        messages.warning(request, "Error: No se enviaron datos...")

    return redirect("devoluciones")


def devoluciones_eliminar(request, id):
	try:
		q = Devoluciones.objects.get(pk=id)
		q.delete()
		messages.success(request, "Devolucion eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("devoluciones")


class RegistrarUsuario(APIView):
    def post(self, request):
        print(request.data)
        if request.method == "POST":
            nombre = request.data["nombre"]
            email = request.data["correo"]
            clave1 = request.data["password"]
            clave2 = request.data["confirmPassword"]
            nick = email
            if nombre == "" or email == "" or clave1 == "" or clave2 == "":
                return Response(data={'message': 'Todos los campos son obligatorios', 'respuesta': 400}, status=400)
            elif not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
				
                return Response(data={'message': 'El correo no es válido', 'respuesta': 400}, status=400)
            elif clave1 != clave2:
                return Response(data={'message': 'Las contraseñas no coinciden', 'respuesta': 400}, status=400)
            else:
                try:
                    q = Usuario(
                        nombre=nombre,
                        email=email,
                        password=make_password(clave1)
                    )
                    q.save()
                except Exception as e:
                    return Response(data={'message': 'El Usuario ya existe', 'respuesta': 409}, status=409)

        # Renderiza la misma página de registro con los mensajes de error
        return Response(data={'message': f'Usuario creado correctamente tu nick es: {nick}', 'respuesta': 201}, status=201)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)


class CustomAuthToken(ObtainAuthToken):
	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data,
		context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['username']
		# traer datos del usuario para bienvenida y ROL
		usuario = Usuario.objects.get(email=user)
		token, created = Token.objects.get_or_create(user=usuario)

		return Response({
			'token': token.key,
			'user': {
				'user_id': usuario.pk,
				'email': usuario.email,
				'nombre': usuario.nombre,
				'rol': usuario.rol,
				'foto': usuario.foto.url
			}
		})
  
def tallas_listar(request):
    t = Tallas.objects.all()
    contexto = {"talla":t}
    return render (request, "tienda/tallas/tallas.html", contexto)

def tallas_form(request):
	return render(request, "tienda/tallas/tallas_form.html")

def tallas_crear(request):
    if request.method == "POST":
        talla = request.POST.get("talla")
        if not re.match(r'^[a-zA-Z0-9]+$', talla):
            messages.error(request, f"La talla solo puede llevar valores numericos o letras")
        
        try:
            q = Tallas(
				talla = talla
			)
            q.save()
            messages.success(request, "Guardado correctamente!!")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("tallas_listar")

def tallas_editar(request, id):
	q = Tallas.objects.get(pk=id)
	contexto = {"talla": q}
	return render(request, "tienda/tallas/tallas_editar.html", contexto)
	         

def tallas_actualizar(request):
	if request.method == "POST":
		id = request.POST.get('id')
		talla = request.POST.get("talla")
		print(talla)
		if not re.match(r'^[a-zA-Z0-9]+$', talla):
				messages.error(request, f"La talla solo puede llevar valores numericos o letras")
		try:
			q = Tallas.objects.get(pk=id)
			q.talla = talla
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("tallas_listar")
			
def tallas_eliminar(request, id):
	try:
		q = Tallas.objects.get(pk=id)
		q.delete()
		messages.success(request, "Talla eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("tallas_listar")
  
def venta_listar(request):
    v = Venta.objects.all(),
    d = DetalleVenta.objects.all(),
    contexto = {"venta": v,"detalle": d}
    return render(request, "tienda/ventas/ventas.html", contexto)

def venta_form(request):
    	return render(request, "tienda/ventas/ventas_form.html")

def cargar_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            return redirect('devoluciones_form')
    else:
        form = ImageUploadForm()
    
    return render(request, 'cargar.html', {'form': form})

from django.utils import timezone

def comentarios_listar(request):
    comentarios = Comentarios.objects.all()
    contexto = {"comentarios":comentarios}
    return render (request, "tienda/comentarios/comentarios_listar.html", contexto)

def comentarios_form(request):
	return render(request, "tienda/comentarios/comentarios_form.html")

def comentarios_crear(request):
    if request.method == "POST":
        comentarios = request.POST.get("comentarios")
        if comentarios is None:
            messages.error(request, "El comentario no puede estar vacío.")
            return redirect("comentarios_form")

        try:
            q = Comentarios(
				comentarios = comentarios,
				descripcion=request.POST.get("descripcion", ""),
				fecha_creacion=timezone.now()
			)
            q.save()
            messages.success(request, "Guardado correctamente!")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("comentarios_listar")


def comentarios_editar(request, id):
	q = Comentarios.objects.get(pk=id)
	contexto = {"comentarios": q}
	return render(request, "tienda/comentarios/comentarios_editar.html", contexto)
	         

def comentarios_actualizar(request):
    if request.method == "POST":
        id = request.POST.get('id')
        comentarios = request.POST.get("comentarios")
        
        try:
            q = Comentarios.objects.get(pk=id)
            if comentarios: 
                q.comentarios = comentarios
                q.save()
                messages.success(request, "Guardado correctamente!!")
            else:
                messages.error(request, "El comentario no puede estar vacío.")
        except Comentarios.DoesNotExist:
            messages.error(request, "Comentario no encontrado.")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect("comentarios_listar")

			
def comentarios_eliminar(request, id):
	try:
		q = Comentarios.objects.get(pk=id)
		q.delete()
		messages.success(request, "Comentario eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")
	return redirect("comentarios_listar")