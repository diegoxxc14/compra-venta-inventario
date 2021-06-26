from django.urls import path, re_path
from django.conf.urls import url
from app import views

urlpatterns = [
    #Página principal (index)
    #path('', views.inicio, name='inicio'),

    path('',views.DashboardView.as_view(), name='inicio'),

    #Bodega Maiz
    path('obtener_maiz/', views.obtener_maiz, name='obtener_maiz'),

    #Compras Maíz
    path('crear_compra/', views.crear_compra, name='crear_compra'),
    path('editar_compra/<int:pk>/', views.editar_compra, name='editar_compra'),
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

    #URLs de la sección Ventas    
    path('gestion_ventas/',views.gestion_ventas, name='gestion_ventas'),
    path('venta_nueva_maiz/',views.venta_nueva_maiz, name='venta_nueva_maiz'),    
    path('buscar_empresa/', views.buscar_empresa, name = 'buscar_empresa'),  
    path('guardar_pesajes_venta/', views.guardar_pesajes_venta, name='guardar_pesajes_venta'),    
    path('buscar_responsable_transporte/', views.buscar_ResponsableTransporte, name='buscar_responsable_transporte'),
    path('editar_venta/<int:pk>/', views.editar_venta, name='editar_venta'),    
    path('editar_pesajes_venta/', views.editar_pesajes_venta, name='editar_pesajes_venta'),
    path('finalizar_venta/', views.finalizar_venta, name='finalizar_venta'),
    path('anular_venta/', views.anular_venta, name='anular_venta'),

    #URLs Autocomplete
    path('buscar_empresa_autocomplete/', views.buscar_empresa_autocomplete, name = 'buscar_empresa_autocomplete'),
    path('buscar_productor_autocomplete/', views.buscar_productor_autocomplete, name = 'buscar_productor_autocomplete'),
    path('buscar_articulo_autocomplete/', views.buscar_articulo_autocomplete, name = 'buscar_articulo_autocomplete'),
    path('buscar_empleado_autocomplete/', views.buscar_empleado_autocomplete, name = 'buscar_empleado_autocomplete'),
    path('buscar_proveedor_autocomplete/', views.buscar_proveedor_autocomplete, name = 'buscar_proveedor_autocomplete'),

    #Transportista
    path('crear_responsableTransporte/',views.CrearResponsableTransporte.as_view(), name='crear_responsableTransporte'),
    path('listar_responsableTransporte/', views.listarResponsableTransporte, name= 'listar_responsableTransporte'),
    path('editar_responsableTransporte/<int:pk>/', views.EditarResponsableTransporte.as_view(), name = 'editar_responsableTransporte'),
    path('eliminar_responsableTransporte/<int:pk>/', views.EliminarResponsableTransporte.as_view(), name = 'eliminar_responsableTransporte'),

    #URLs para la generación de reportes
    path('reportes_compras/', views.reportes_compras, name='reportes_compras'),
    path('imprimir_compras/', views.imprimir_compras, name='imprimir_compras'),
    path('reportes_ventas/', views.reportes_ventas, name='reportes_ventas'),
    path('imprimir_ventas/', views.imprimir_ventas, name='imprimir_ventas'),
    path('reporte_facturacion_compras/', views.reportes_facturacion_compras, name='reporte_facturacion_compras'),
    path('imprimir_facturacion_compras/', views.imprimir_facturacion_compras, name='imprimir_facturacion_compras'),
    path('reporte_facturacion_ventas/', views.reportes_facturacion_ventas, name='reporte_facturacion_ventas'),
    path('imprimir_facturacion_ventas/', views.imprimir_facturacion_ventas, name='imprimir_facturacion_ventas'),
    path('reporte_facturacion_transporte/', views.reportes_facturacion_transporte, name='reporte_facturacion_transporte'),
    path('imprimir_facturacion_transporte/', views.imprimir_facturacion_transporte, name='imprimir_facturacion_transporte'),

    #path('imprimir_ingreso_pdf/', views.imprimir_ingreso_pdf, name='imprimir_ingreso_pdf'),
    #URLs 
    path('ingresar_articulo/ingreso_documento_pdf/<int:pk>/', views.ImprimirIngresoPdfView.as_view(), name='ingreso_documento_pdf'),
    path('salida_articulo/salida_documento_pdf/<int:pk>/', views.ImprimirSalidaPdfView.as_view(), name='salida_documento_pdf'),
    path('inventario_general/inventario_documento_pdf/', views.ImprimirInventarioPdfView.as_view(), name='inventario_documento_pdf'),
    path('pesaje_compra_doc_pdf/<int:pk>/', views.ImprimirPesajeCompraPdfView.as_view(), name='pesaje_compra_doc_pdf'),
    path('pesaje_venta_doc_pdf/<int:pk>/', views.ImprimirPesajeVentaPdfView.as_view(), name='pesaje_venta_doc_pdf'),
    

    #URLs para la seccion de inventario de insumos e implementos
    path('inventario_general/',views.inventario_general, name='inventario_general'),
    path('listar_bodega/',views.listar_bodega, name='listar_bodega'),
    path('imprimir_bodega/', views.imprimir_bodega , name='imprimir_bodega'),

    
    # URLS para Articulo
    path('crear_articulo/',views.CrearArticulo.as_view(), name='crear_articulo'),     
    path('editar_articulo/<int:pk>/', views.EditarArticulo.as_view(), name = 'editar_articulo'),
    path('eliminar_articulo/<int:pk>/', views.EliminarArticulo.as_view(), name = 'eliminar_articulo'),
    path('listar_articulo/',views.listar_articulo, name='listar_articulo'),  

    path('ingresar_articulo/',views.ingresar_articulo, name='ingresar_articulo'),
    path('guardar_ingreso_articulos/', views.guardar_ingreso_articulos, name='guardar_ingreso_articulos'),
    path('salida_articulo/',views.salida_articulo, name='salida_articulo'),
    path('guardar_salida_articulos/', views.guardar_salida_articulos, name='guardar_salida_articulos'),

    #URLS para Categoria
    path('crear_categoria/',views.CrearCategoria.as_view(), name='crear_categoria'),    
    path('listar_categoria/',views.listar_categoria, name='listar_categoria'),        
    path('editar_categoria/<int:pk>/', views.EditarCategoria.as_view(), name = 'editar_categoria'),
    path('eliminar_categoria/<int:pk>/', views.EliminarCategoria.as_view(), name = 'eliminar_categoria'),
    #path('eliminar_categoria/<int:pk>/', views.EliminarCategoria, name = 'eliminar_categoria'),

    #URLs para la sección de proveedor
    path('crear_proveedor/',views.CrearProveedor.as_view(), name='crear_proveedor'),
    path('listar_proveedor/',views.listar_proveedor, name='listar_proveedor'),
    path('editar_proveedor/<int:pk>/', views.EditarProveedor.as_view(), name = 'editar_proveedor'),
    path('eliminar_proveedor/<int:pk>/', views.EliminarProveedor.as_view(), name = 'eliminar_proveedor'),
    
    
    #URLs para la seccion de empleado
    path('crear_empleado/',views.CrearEmpleado.as_view(), name='crear_empleado'),    
    path('listar_empleado/',views.listar_empleado, name='listar_empleado'),
    path('editar_empleado/<int:pk>/', views.EditarEmpleado.as_view(), name = 'editar_empleado'),
    path('eliminar_empleado/<int:pk>/', views.EliminarEmpleado.as_view(), name = 'eliminar_empleado'),
    
    #facturacion compras
    path('crear_facturacion/',views.facturacion_compra, name='facturacion_compra'),
    path('buscar_pesaje_compra/',views.buscar_PesajesCompra, name='buscar_pesaje_compra'),
    path('obtener_compras/',views.obtener_compras_pendientes, name='obtener_compras'),
    path('guardar_documento/',views.guardar_documento, name='guardar_documento'),
    #facturacion ventas
    path('crear_facturacion_ventas/',views.facturacion_venta, name='facturacion_venta'),
    path('obtener_ventas/',views.obtener_ventas_pendientes, name='obtener_ventas'),
    path('guardar_factura_venta/',views.guardar_documento_venta, name='guardar_factura_venta'),
    #facturación transporte
    path('crear_facturacion_transporte/',views.facturacion_transporte, name='facturacion_transporte'),
    path('obtener_ventas_facturacion/',views.obtener_ventas_pendientes_facturacion, name='obtener_ventas_facturacion'),
    path('guardar_factura_transporte/',views.guardar_documento_transporte, name='guardar_factura_transporte'),



    re_path(r'^.*\.html', views.gentella_html, name='gentella'),

]
