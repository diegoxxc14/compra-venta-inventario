from django.urls import path, re_path
from django.conf.urls import url
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    #URLs de la seccion compras
    path('compra_maiz/', views.compra_maiz, name='compra_m'),
    path('editar_compra/<int:pk>/', views.editar_compra, name='editar_compra'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
    path('anular_compra/', views.anular_compra, name='anular_compra'),
    path('guardar_pesajes/', views.guardar_pesajes, name='guardar_pesajes'),
    path('editar_pesajes/', views.editar_pesajes, name='editar_pesajes'),

    path('ingresocompras/',views.ingreso_compras, name='ingresar_com'),
    path('nuevoproductor/',views.nuevo_productor, name='nuevo_prod'),
    #path('crear_productor/',views.crear_productor, name='crear_productor'),

    path('buscar_productor/', views.buscar_productor, name = 'buscar_productor'),

    path('crear_productor/',views.CrearProductor.as_view(), name='crear_productor'),
    path('listar_productor/', views.listarProductor, name= 'listar_productor'),
    path('editar_productor/<int:pk>/', views.EditarProductor.as_view(), name = 'editar_productor'),
    path('eliminar_productor/<int:pk>/',views.EliminarProductor.as_view(), name = 'eliminar_productor'),

    #URLs de la sección Ventas    
    path('crear_empresa/',views.CrearEmpresa.as_view(), name='crear_empresa'),
    path('listar_empresa/', views.listarEmpresa, name= 'listar_empresa'),
    path('editar_empresa/<int:pk>/', views.EditarEmpresa.as_view(), name = 'editar_empresa'),
    path('eliminar_empresa/<int:pk>/',views.EliminarEmpresa.as_view(), name = 'eliminar_empresa'),
    #URLs de la sección Responsable Transportista
    path('crear_responsableTransporte/',views.CrearResponsableTransporte.as_view(), name='crear_responsableTransporte'),
    path('listar_responsableTransporte/', views.listarResponsableTransporte, name= 'listar_responsableTransporte'),
    path('editar_responsableTransporte/<int:pk>/', views.EditarResponsableTransporte.as_view(), name = 'editar_responsableTransporte'),
    path('eliminar_responsableTransporte/<int:pk>/',views.EliminarResponsableTransporte.as_view(), name = 'eliminar_responsableTransporte'),
    
    #URLs de la sección inventarios insumos
    path('crear_proveedor/',views.crear_proveedor, name='crear_proveedor'),
    path('crear_articulo/', views.crear_articulo, name='crear_articulo'),
    #path('crear_inventario/',views.crear_inventario, name='crear_inventario'),
    #path('editar_inventario/<int:pk>/', views.editar_inventario, name='editar_inventario'),
    path('crear_inventario/',views.CrearInventario.as_view(), name = 'crear_inventario'),    
    path('editar_inventario/<int:pk>/', views.EditarInventario.as_view(), name = 'editar_inventario'),
    path('eliminar_inventario/<int:pk>/',views.EliminarInventario.as_view(), name = 'eliminar_inventario'),
    path('listar_inventario/', views.ListarInventario.as_view(), name= 'listar_inventario'),

    path('listar_ventas/', views.listarVentas, name='listar_ventas'),
    path('reportes_compras/', views.reportes_compras, name='reportes_compras'),
    path('imprimir_compras/', views.imprimir_compras, name='imprimir_compras'),

    
    #url(r'^editar_inventario/(?P<id_inventario>\d+)/$', views.editar_inventario, name='editar_inventario'),
    #path('crear_articulo1/', views.CrearArticuloView.as_view(), name='crear_articulo1'),
    #URLs de la sección inventarios
    path('listacompras/',views.lista_compras, name='lista_c'),
    path('listaventas/',views.lista_ventas, name='lista_v'),
    path('lista_implementos/',views.lista_insumos_e_implementos, name='lista_implementos'),
    path('nuevoproveedor/', views.nuevo_proveedor, name='nuevo_prov'),
    path('registroinventario/',views.registro_inventario, name='registro_i'),
    
    #URLs de la sección Inventarios de Insumos e Implementos
    path('ajusteinventario/',views.ajuste_inventario, name='ajuste_i'),
    path('egresoinventario/',views.salida_inventario, name='salida_i'),
    path('ingresoinventario/',views.ingreso_inventario, name='ingreso_i'),
    path('editarinventario/',views.editar_inventario, name='editar_i'),


    #Facturas Compra
    path('facturacompra/',views.factura_compra, name='factura_compra'),

    re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    path('', views.inicio, name='inicio'),
    
]
