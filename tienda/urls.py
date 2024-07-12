from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls


router = routers.DefaultRouter()
router.register(r'categoria', views.CategoriaViewSet)
router.register(r'producto', views.ProductoViewSet)
router.register(r'usuario', views.UsuarioViewSet)
router.register(r'categoria-etiqueta', views.CategoriaEtiquetaViewSet)
router.register(r'subcategoria-etiqueta', views.SubCategoriaEtiquetaViewSet)
router.register(r'producto-subcategoria', views.ProductoSubCategoriaViewSet)
router.register(r'venta', views.VentaViewSet)
router.register(r'detalle-venta', views.DetalleVentaViewSet)

urlpatterns = [
	path('index/', views.index, name="index"),
	path('', views.inicio, name="inicio"),
    
	#API
    path('api/1.0/', include(router.urls)),

	# Autenticación de usuarios del sistema
	path('login/', views.login, name="login"),
	path('logout/', views.logout, name="logout"),
	path("registro/", views.registro, name="registro"),
	path('registrar_usuario/', views.registrar_usuario, name="registrar_usuario"),
    path("recuperar_clave/", views.recuperar_clave, name="recuperar_clave"),
	path("verificar_recuperar/", views.verificar_recuperar, name="verificar_recuperar"),
 
 	# Usuarios CRUD
	
	path("usuarios_listar/", views.usuarios, name="usuarios_listar"),
	path("usuarios_form/", views.usuarios_form, name="usuarios_form"),
	path("usuarios_crear/", views.usuarios_crear, name="usuarios_crear"),
	path("usuarios_eliminar/<int:id>", views.usuarios_eliminar, name="usuarios_eliminar"),
	path("usuarios_formulario_editar/<int:id>", views.usuarios_formulario_editar, name="usuarios_formulario_editar"),
	path("usuarios_actualizar/", views.usuarios_actualizar, name="usuarios_actualizar"),
	

	# CRUD de Categorías
	path("categorias_listar/", views.categorias, name="categorias_listar"),
	path("categorias_form/", views.categorias_form, name="categorias_form"),
	path("categorias_crear/", views.categorias_crear, name="categorias_crear"),
	path("categorias_eliminar/<int:id>", views.categorias_eliminar, name="categorias_eliminar"),
	path("categorias_formulario_editar/<int:id>", views.categorias_formulario_editar, name="categorias_formulario_editar"),
	path("categorias_actualizar/", views.categorias_actualizar, name="categorias_actualizar"),

	# CRUD de Productos
	path("productos_listar/", views.productos, name="productos_listar"),
	path("productos_form/", views.productos_form, name="productos_form"),
	path("productos_crear/", views.productos_crear, name="productos_crear"),
	path("productos_eliminar/<int:id>", views.productos_eliminar, name="productos_eliminar"),
	path("productos_formulario_editar/<int:id>", views.productos_formulario_editar, name="productos_formulario_editar"),
	path("productos_actualizar/", views.productos_actualizar, name="productos_actualizar"),

	path("ver_perfil/", views.ver_perfil, name="ver_perfil"),
	path("cc_formulario/", views.cambio_clave_formulario, name="cc_formulario"),
	path("cambiar_clave/", views.cambiar_clave, name="cambiar_clave"),

	# carrito de compra
	path("carrito_add/", views.carrito_add, name="carrito_add"),
	path("carrito_ver/", views.carrito_ver, name="carrito_ver"),
	path("vaciar_carrito/", views.vaciar_carrito, name="vaciar_carrito"),
	path("eliminar_item_carrito/<int:id_producto>", views.eliminar_item_carrito, name="eliminar_item_carrito"),
	path("actualizar_totales_carrito/<int:id_producto>/", views.actualizar_totales_carrito, name="actualizar_totales_carrito"),
 
	#ventas
	path("realizar_venta/", views.realizar_venta, name="realizar_venta"),
	path("prueba_correo/", views.prueba_correo, name="prueba_correo"),
    

	#etiquetas
    path("etiquetas_listar/", views.etiquetas_listar, name="etiquetas_listar"),
    path("etiquetas_crear/", views.etiquetas_crear, name="etiquetas_crear"),
    path("etiquetas_eliminar/<int:id>", views.etiquetas_eliminar, name="etiquetas_eliminar"),
    path("etiquetas_form_editar/<int:id>", views.etiquetas_formulario_editar, name="etiquetas_form_editar"),
    path("etiquetas_actualizar", views.etiquetas_actualizar, name="etiquetas_actualizar"),
    path("etiquetas_form/", views.etiquetas_form, name="etiquetas_form"),

	#Terminos y condiciones
 	path("term_y_cond/", views.term_y_cond, name="term_y_cond"),
  
  
	# CRUD de Devoluciones
	path("devoluciones/", views.devoluciones, name="devoluciones"),
	path("devoluciones_form/", views.devoluciones_form, name="devoluciones_form"),
	path("devoluciones_crear/", views.devoluciones_crear, name="devoluciones_crear"),
	path("devoluciones_formulario_editar/<int:id>", views.devoluciones_formulario_editar, name="devoluciones_formulario_editar"),
	path("devoluciones_actualizar/", views.devoluciones_actualizar, name="devoluciones_actualizar"),
	path("devoluciones_eliminar/<int:id>", views.devoluciones_eliminar, name="devoluciones_eliminar"),
]
