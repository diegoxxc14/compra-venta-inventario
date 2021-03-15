from django.urls import path, re_path
from django.conf.urls import url
from app import views

urlpatterns = [
    #Página principal (index)
    path('', views.inicio, name='inicio'),

    #Compras Maíz
    path('crear_compra/', views.crear_compra, name='crear_compra'),
    path('editar_compra/<int:pk>/', views.editar_compra, name='editar_compra'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
    path('anular_compra/', views.anular_compra, name='anular_compra'),
    path('guardar_pesajes/', views.guardar_pesajes, name='guardar_pesajes'),
    path('editar_pesajes/', views.editar_pesajes, name='editar_pesajes'),
    path('gestion_compras/',views.gestion_compras, name='gestion_compras'),

    #Productor
    path('buscar_productor/', views.buscar_productor, name = 'buscar_productor'),
    path('crear_productor/',views.CrearProductor.as_view(), name='crear_productor'),
    path('listar_productores/', views.listar_productores, name= 'listar_productores'),
    path('editar_productor/<int:pk>/', views.EditarProductor.as_view(), name = 'editar_productor'),
    path('eliminar_productor/<int:pk>/',views.EliminarProductor.as_view(), name = 'eliminar_productor'),

    #Ventas    
    path('crear_empresa/',views.CrearEmpresa.as_view(), name='crear_empresa'),
    path('listar_empresas/', views.listar_empresas, name= 'listar_empresas'),
    path('editar_empresa/<int:pk>/', views.EditarEmpresa.as_view(), name = 'editar_empresa'),
    path('eliminar_empresa/<int:pk>/',views.EliminarEmpresa.as_view(), name = 'eliminar_empresa'),

    #Transportista
    path('crear_responsableTransporte/',views.CrearResponsableTransporte.as_view(), name='crear_responsableTransporte'),
    path('listar_responsableTransporte/', views.listarResponsableTransporte, name= 'listar_responsableTransporte'),
    path('editar_responsableTransporte/<int:pk>/', views.EditarResponsableTransporte.as_view(), name = 'editar_responsableTransporte'),
    path('eliminar_responsableTransporte/<int:pk>/',views.EliminarResponsableTransporte.as_view(), name = 'eliminar_responsableTransporte'),
    
    #URLs de la sección inventarios insumos
    path('crear_proveedor/',views.crear_proveedor, name='crear_proveedor'),
    path('crear_articulo/', views.crear_articulo, name='crear_articulo'),
    path('crear_inventario/',views.CrearInventario.as_view(), name = 'crear_inventario'),    
    path('editar_inventario/<int:pk>/', views.EditarInventario.as_view(), name = 'editar_inventario'),
    path('eliminar_inventario/<int:pk>/',views.EliminarInventario.as_view(), name = 'eliminar_inventario'),
    path('listar_inventario/', views.ListarInventario.as_view(), name= 'listar_inventario'),

    path('listar_ventas/', views.listarVentas, name='listar_ventas'),
    path('reportes_compras/', views.reportes_compras, name='reportes_compras'),
    path('imprimir_compras/', views.imprimir_compras, name='imprimir_compras'),

    #URLs de la sección inventarios    
    path('listaventas/',views.lista_ventas, name='lista_v'),
    path('lista_implementos/',views.lista_insumos_e_implementos, name='lista_implementos'),
    path('nuevoproveedor/', views.nuevo_proveedor, name='nuevo_prov'),
    path('registroinventario/',views.registro_inventario, name='registro_i'),
    
    #URLs de la sección Inventarios de Insumos e Implementos
    path('ajusteinventario/',views.ajuste_inventario, name='ajuste_i'),
    path('egresoinventario/',views.salida_inventario, name='salida_i'),
    path('ingresoinventario/',views.ingreso_inventario, name='ingreso_i'),
    path('editarinventario/',views.editar_inventario, name='editar_i'),

    path('crear_facturacion/',views.facturacion_compra, name='facturacion_compra'),

    re_path(r'^.*\.html', views.gentella_html, name='gentella'),

]
