from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.forms import model_to_dict#agregamos la nueva forms

# Create your models here.
UNIDAD = [
    ('Pieza','Pieza'),    
    ('Metro','Metro'),
    ('Litro','Litro'),
    ('Galón','Galón'),
    ('Caneca','Caneca'),
    ('Libra','Libra'),
    ('kilogramo','Kilogramo'),
    ('Quintal','Quintal'),
]

class Productor(models.Model):
    identificacion = models.CharField(max_length=10, unique=True, blank=False, null=False)
    nombres = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Productor'
        verbose_name_plural = 'Productores'
        ordering = ['nombres']
    
    def __str__(self):
        return self.nombres

    def toJSON(self):
        item = model_to_dict(self)
        return item

class BodegaMaiz(models.Model): #Registro del stock en Bodega
    fecha = models.DateTimeField(auto_now_add=True) #Guarda la fecha de creación de un objeto
    tipoMovimiento = models.CharField(max_length=25)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    vigente = models.BooleanField(default=True) #En caso de eliminación o edición
    idCompraMaiz = models.ForeignKey('CompraMaiz', on_delete=models.CASCADE, null=True)
    idVentaMaiz = models.ForeignKey('VentaMaiz', on_delete=models.CASCADE, null=True)

class ResponsableTransporte(models.Model):
    identificacion = models.CharField(max_length=10,unique=True, blank=False, null=False)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono =models.CharField(max_length=10)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    placaTrailer = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Responsable Transporte'
        verbose_name_plural = 'Responsables Transporte'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

class CompraMaiz(models.Model): #Datos de la Compra
    fechaCompra = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)
    observacion = models.CharField(max_length=100)
    humedad = models.IntegerField() #Dato constante
    impureza = models.IntegerField() #Dato constante
    valida = models.BooleanField(default=True) #Si la compra es válida, no eliminada
    pendiente = models.BooleanField(default=True) #Si la compra estará pendiente o no de facturar
    total = models.DecimalField(max_digits=7, decimal_places=2)
    idProductor = models.ForeignKey('Productor',on_delete=models.PROTECT)
    idDocumentoCompra = models.ForeignKey('DocumentoCompra', on_delete = models.CASCADE, null=True)
    
    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.idProductor

    def toJSON(self):
        item = model_to_dict(self)
        item['total'] = format(self.total, '.2f')
        item['fechaCompra'] = self.fechaCompra.strftime('%Y-%m-%d')
        item['pes'] = [i.toJSON() for i in self.pesajecompramaiz_set.get(vigente=True)]#get(vigente=true)#set.all()
        return item

class DocumentoCompra(models.Model):
    tipoDocumento = models.CharField(max_length=25) #tipo de documento de compra factura o nota de venta
    numeroDocumento = models.CharField(max_length=12, null=False) 
    fechaEmision = models.DateField()
    cantidad = models.DecimalField(max_digits=7,decimal_places=2)
    preciounitario = models.DecimalField(max_digits=4,decimal_places=2)
    precioTotal = models.DecimalField(max_digits=8,decimal_places=2)
    idProductor = models.ForeignKey('Productor', on_delete=models.PROTECT)#para probar

class PesajeCompraMaiz(models.Model): #Los Pesajes correspondientes a una Compra
    fechaPesaje = models.DateTimeField() #No es "auto_now_add" porque la fecha se toma antes de guardar
    pesoBruto = models.IntegerField()
    pesoTara = models.IntegerField()
    pesoNeto = models.IntegerField()
    factorConversion = models.DecimalField(max_digits=4,decimal_places=2)
    pesoQuintales = models.DecimalField(max_digits=7,decimal_places=2)
    vigente = models.BooleanField(default=True) #Si cada pesaje está vigente en la compra
    idCompraMaiz = models.ForeignKey('CompraMaiz', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'PesajeCompraMaiz'
        verbose_name_plural = 'PesajeCompraMaiz'
        ordering = ['fechaPesaje']
    
    def __str__(self):
        return self.pesoQuintales
        
    def toJSON(self):
        item = model_to_dict(self)
        item['idCompraMaiz'] = self.idCompraMaiz.toJSON()
        return item

class PesajeVentaMaiz(models.Model):
    fechaPesaje = models.DateField()
    pesoBruto = models.IntegerField()
    pesoTara = models.IntegerField()
    pesoNeto = models.IntegerField()
    factorConversion = models.DecimalField(max_digits=4,decimal_places=2)
    pesoQuintales = models.DecimalField(max_digits=7,decimal_places=2)
    vigente = models.BooleanField(default=True) #Si cada pesaje está vigente en la compra   
    idVentaMaiz = models.ForeignKey('VentaMaiz', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'PesajeVentaMaiz'
        verbose_name_plural = 'PesajeVentaMaiz'
        ordering = ['fechaPesaje']
    
    def __str__(self):
        return self.pesoQuintales
        
    def toJSON(self):
        item = model_to_dict(self)
        item['idVentaMaiz'] = self.idVentaMaiz.toJSON()
        return item

class Empresa(models.Model):
    ruc = models.CharField(max_length=13,unique=True, blank=False, null=False) 
    razonSocial = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['razonSocial']
    
    def __str__(self):
        return self.razonSocial

    def toJSON(self):
        item = model_to_dict(self)
        return item

class VentaMaiz(models.Model):
    fechaVenta = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)    
    observaciones = models.CharField(max_length=100)
    humedad = models.IntegerField() #Dato constante
    impureza = models.IntegerField() #Dato constante
    valida = models.BooleanField(default=True) #Si la venta es válida, no eliminada
    pendiente = models.BooleanField(default=True) #Si la venta estará pendiente de facturacion o no
    statusFactura = models.BooleanField(default=True) #Estado de facturacion True pendiente de facturacion###########################
    total = models.DecimalField(max_digits=7, decimal_places=2)
    idEmpresa = models.ForeignKey('Empresa', on_delete=models.PROTECT)
    idResponsableTransporte = models.ForeignKey('ResponsableTransporte', on_delete=models.PROTECT)
    idFacturaVenta = models.ForeignKey('FacturaVenta', on_delete = models.CASCADE, null=True)
    idFacturaTransporte = models.ForeignKey('FacturaTransporte', on_delete = models.CASCADE, null=True)

    class Meta:  #cambios
        ordering = ['-pk']
    
    def __str__(self):
        return self.idEmpresa

    def toJSON(self):
        item = model_to_dict(self)
        item['total'] = format(self.total, '.2f')
        item['fechaVenta'] = self.fechaVenta.strftime('%Y-%m-%d')
        item['idFacturaVenta'] = self.idFacturaVenta.toJSON()
        item['pes'] = [i.toJSON() for i in self.pesajeventamaiz_set.get(vigente=True)]#get(vigente=true)#set.all()
        return item
        
class FacturaVenta(models.Model):
    numeroFactura = models.CharField(max_length=12, null=False)
    fechaEmision = models.DateField()
    cantidad = models.DecimalField(max_digits=7,decimal_places=2)
    preciounitario = models.DecimalField(max_digits=4,decimal_places=2)
    precioTotal = models.DecimalField(max_digits=8,decimal_places=2)
    idEmpresa = models.ForeignKey('Empresa', on_delete=models.PROTECT)#para probar

    class Meta:
        verbose_name = 'facturaVenta'
        verbose_name_plural = 'facturasVenta'
        ordering = ['fechaEmision']
    
    def __str__(self):
        return self.numeroFactura

    def toJSON(self):
        item = model_to_dict(self)
        return item

    
class FacturaTransporte(models.Model):
    numerofactura = models.CharField(max_length=12, null=False)
    fechaEmision = models.DateField()
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    preciounitario = models.DecimalField(max_digits=4,decimal_places=2)
    precioTotal = models.DecimalField(max_digits=8,decimal_places=2)
    idResponsableTransporte = models.ForeignKey('ResponsableTransporte', on_delete=models.PROTECT)#para probarresponsable transporte

    class Meta:
        verbose_name = 'facturaTransporte'
        verbose_name_plural = 'facturasTransporte'
        ordering = ['fechaEmision']
    
    def __str__(self):
        return self.numeroFactura

    def toJSON(self):
        item = model_to_dict(self)
        return item


#creamos un tabla Categoria que se debe cambiar en el modelo de base de datos 
    #idProveedor = models.ForeignKey('Proveedor', on_delete = models.CASCADE)
class Categoria(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nombre']

class Articulo(models.Model):
    idCategoria = models.ForeignKey('Categoria',null=True, blank=True, on_delete=models.PROTECT) # , on_delete = models.CASCADE
    descripcion = models.CharField(max_length=100,unique=True)
    stock = models.IntegerField(default=0, verbose_name='Stock')#default=0, verbose_name='Stock'
    unidadMedida = models.CharField(max_length=100, choices=UNIDAD)

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'
        ordering = ['descripcion']

    def __str__(self):
        return self.descripcion        
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

#cambiamos base de datos
class IngresoArticulo(models.Model):
    idProveedor = models.ForeignKey('Proveedor', on_delete = models.PROTECT)    
    fecha = models.DateField(default=datetime.now)

    def __str__(self):
        return self.idProveedor.razonSocial        
    
    def toJSON(self):
        item = model_to_dict(self)
        item['det'] = [i.toJSON() for i in self.detalleingresoarticulos_set.all()]
        return item
    
class DetalleIngresoArticulos(models.Model):
    idIngreso = models.ForeignKey('IngresoArticulo', on_delete = models.CASCADE) 
    idArticulo = models.ForeignKey('Articulo', on_delete = models.PROTECT)
    cantidad = models.IntegerField(blank = False, null = False)

    def __str__(self):
        return self.idArticulo.descripcion        
    
    def toJSON(self):
        item = model_to_dict(self)
        item['idArticulo'] = self.idArticulo.toJSON()
        item['cantidad'] = self.cantidad
        return item

class SalidaArticulo(models.Model):
    idEmpleado = models.ForeignKey('Empleado', on_delete = models.PROTECT)
    fecha = models.DateField(default=datetime.now)

    def __str__(self):
        return self.idEmpleado.nombres        
    
    def toJSON(self):
        item = model_to_dict(self)
        item['det'] = [i.toJSON() for i in self.detallesalidaarticulos_set.all()]
        return item

class DetalleSalidaArticulos(models.Model):
    idSalida = models.ForeignKey('SalidaArticulo', on_delete = models.CASCADE) 
    idArticulo = models.ForeignKey('Articulo', on_delete = models.PROTECT)
    cantidad = models.IntegerField(blank = False, null = False)

    def __str__(self):
        return self.idArticulo.descripcion        
    
    def toJSON(self):
        item = model_to_dict(self)
        item['idArticulo'] = self.idArticulo.toJSON()
        item['cantidad'] = self.cantidad
        return item

class Proveedor(models.Model):
    ruc = models.CharField(max_length=13,unique=True, blank=False, null=False)
    razonSocial = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(max_length=100, blank=True, null=True)

    class Meta:
      verbose_name = 'Proveedor'
      verbose_name_plural = 'Proveedores'
    
    def __str__(self):
      return self.razonSocial
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

class Empleado(models.Model):
    identificacion = models.CharField(max_length=10,unique=True, blank=False, null=False)
    nombres = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, blank=True, null=True)

    def __str__(self):
      return self.nombres
    
    def toJSON(self):
        item = model_to_dict(self)
        return item