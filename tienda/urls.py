from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'categoria', views.CategoriaViewSet)
router.register(r'producto', views.ProductoViewSet)
router.register(r'usuario', views.UsuarioViewSet)
router.register(r'categoria-etiqueta', views.CategoriaEtiquetaViewSet)
router.register(r'subcategoria-etiqueta', views.SubCategoriaEtiquetaViewSet)
router.register(r'producto-subcategoria', views.ProductoSubCategoriaViewSet)
router.register(r'venta', views.VentaViewSet)
router.register(r'detalleVenta', views.DetalleVentaViewSet)
router.register(r'devoluviones', views.DevolucionesViewSet)

urlpatterns = [
    path('index/', views.index, name="index"),
    path('', views.inicio, name="inicio"),

    # API
    path('api/1.0/', include(router.urls)),
    path('api/1.0/token-auth/', views.CustomAuthToken.as_view()),
    path('api/1.0/api-auth/', include('rest_framework.urls')),
    path('api/1.0/registrar_usuario/', views.RegistrarUsuario.as_view(), name='registrar_usuario'),

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

    # Perfil
    path("ver_perfil/", views.ver_perfil, name="ver_perfil"),
    path("cc_formulario/", views.cambio_clave_formulario, name="cc_formulario"),
    path("cambiar_clave/", views.cambiar_clave, name="cambiar_clave"),

    # Carrito de compra
    path("carrito_add/", views.carrito_add, name="carrito_add"),
    path("carrito_ver/", views.carrito_ver, name="carrito_ver"),
    path("vaciar_carrito/", views.vaciar_carrito, name="vaciar_carrito"),
    path("eliminar_item_carrito/<int:id_producto>", views.eliminar_item_carrito, name="eliminar_item_carrito"),
    path("actualizar_totales_carrito/<int:id_producto>/", views.actualizar_totales_carrito, name="actualizar_totales_carrito"),

    # Ventas
    path("realizar_venta/", views.realizar_venta, name="realizar_venta"),
    path("ventas_ver/", views.ventas_ver, name="ventas_ver"),
    path("prueba_correo/", views.prueba_correo, name="prueba_correo"),

    # Pedidos
    path("realizar_pedido/", views.realizar_pedido, name="realizar_pedido"),
    path("pedido_ver/", views.pedido_ver, name="pedido_ver"),
    path("pedido_eliminar/<int:id>", views.pedido_eliminar, name="pedido_eliminar"),

    # Etiquetas
    path("etiquetas_listar/", views.etiquetas_listar, name="etiquetas_listar"),
    path("etiquetas_crear/", views.etiquetas_crear, name="etiquetas_crear"),
    path("etiquetas_eliminar/<int:id>", views.etiquetas_eliminar, name="etiquetas_eliminar"),
    path("etiquetas_form_editar/<int:id>", views.etiquetas_formulario_editar, name="etiquetas_form_editar"),
    path("etiquetas_actualizar", views.etiquetas_actualizar, name="etiquetas_actualizar"),
    path("etiquetas_form/", views.etiquetas_form, name="etiquetas_form"),

    # Términos y condiciones
    path("term_y_cond/", views.term_y_cond, name="term_y_cond"),

    # Tallas
    path("tallas_listar/", views.tallas_listar, name="tallas_listar"),
    path("talla_form/", views.tallas_form, name="tallas_form"),
    path("tallas_crear/", views.tallas_crear, name="tallas_crear"),
    path("tallas_actualizar/", views.tallas_actualizar, name="tallas_actualizar"),
    path("tallas_eliminar/<int:id>", views.tallas_eliminar, name="tallas_eliminar"),
    path("tallas_editar/<int:id>", views.tallas_editar, name="tallas_editar"),

    # Ventas
    path("venta_listar/", views.venta_listar, name="venta_listar"),

    # CRUD de Devoluciones
    path("devoluciones/", views.devoluciones, name="devoluciones"),
    path('devoluciones/estado/<int:id>/', views.estado_devolucion, name='estado_devolucion'),
    path("ver_devolucion/", views.ver_devolucion, name="ver_devolucion"),
    path('cargar/', views.cargar_image, name='cargar_image'),

	# Devoluciones
    path("devoluciones_form/", views.devoluciones_form, name="devoluciones_form"),
    path("devoluciones_crear/", views.devoluciones_crear, name="devoluciones_crear"),
    path("devoluciones_formulario_editar/<int:id>", views.devoluciones_formulario_editar, name="devoluciones_formulario_editar"),
    path("devoluciones_actualizar/", views.devoluciones_actualizar, name="devoluciones_actualizar"),
    path("devoluciones_eliminar/<int:id>", views.devoluciones_eliminar, name="devoluciones_eliminar"),
	path('devoluciones/estado/<int:id>/', views.estado_devolucion, name='estado_devolucion'),

	# Comentarios
    path('comentarios_listar/', views.comentarios_listar, name='comentarios_listar'),
    path("comentarios_form/", views.comentarios_form, name="comentarios_form"),
    path("comentarios_crear/", views.comentarios_crear, name="comentarios_crear"),
    path("comentarios_actualizar/", views.comentarios_actualizar, name="comentarios_actualizar"),
    path('comentarios/eliminar/<int:id>/', views.comentarios_eliminar, name='comentarios_eliminar'),
    path("comentarios_editar/<int:id>", views.comentarios_editar, name="comentarios_editar"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)