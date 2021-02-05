from __future__ import unicode_literals
from django.db import models

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

class BodegaMaiz(models.Model): #Registro del stock en Bodega
    fecha = models.DateTimeField(auto_now_add=True) #Guarda la fecha de creación de un objeto
    tipoMovimiento = models.CharField(max_length=25)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    stockMaiz = models.DecimalField(max_digits=7, decimal_places=2)
    idCompraMaiz = models.ForeignKey('CompraMaiz', on_delete=models.CASCADE)

class ResponsableTransporte(models.Model):
    identificacion = models.CharField(max_length=10,unique=True, blank=False, null=False)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono =models.CharField(max_length=10)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    placaTrailer = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class CompraMaiz(models.Model): #Datos de la Compra
    fechaCompra = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)
    observacion = models.CharField(max_length=100)
    humedad = models.IntegerField() #Dato constante
    impureza = models.IntegerField() #Dato constante
    valida = models.BooleanField(default=True) #Si la compra es válida, no eliminada
    pendiente = models.BooleanField(default=True) #Si la compra estará pendiente o no
    total = models.DecimalField(max_digits=7, decimal_places=2)
    idProductor = models.ForeignKey('Productor', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-pk']

class DocumentoCompra(models.Model):
    tipoDocumento = models.CharField(max_length=25)
    numeroDocumento = models.IntegerField()
    fechaEmision = models.DateField()
    cantidad = models.DecimalField(max_digits=7,decimal_places=2)
    preciounitario = models.DecimalField(max_digits=4,decimal_places=2)
    precioTotal = models.DecimalField(max_digits=8,decimal_places=2)
    estado = models.CharField(max_length=25)
    tipoPago = models.CharField(max_length=25)
    idCompraMaiz = models.ForeignKey('CompraMaiz', on_delete = models.CASCADE)

class PesajeCompraMaiz(models.Model): #Los Pesajes correspondientes a una Compra
    fechaPesaje = models.DateTimeField() #No es "auto_now_add" porque la fecha se toma antes de guardar
    pesoBruto = models.IntegerField()
    pesoTara = models.IntegerField()
    pesoNeto = models.IntegerField()
    factorConversion = models.DecimalField(max_digits=4,decimal_places=2)
    pesoQuintales = models.DecimalField(max_digits=7,decimal_places=2)
    vigente = models.BooleanField(default=True) #Si cada pesaje está vigente en la compra
    idCompraMaiz = models.ForeignKey('CompraMaiz', on_delete = models.CASCADE)

class PesajeVentaMaiz(models.Model):
    fechaPesaje = models.DateField()
    pesoBruto = models.IntegerField()
    pesoTara = models.IntegerField()
    pesoNeto = models.IntegerField()
    factorConversion = models.DecimalField(max_digits=4,decimal_places=2)
    pesoQuintales = models.DecimalField(max_digits=7,decimal_places=2)
    idVentaMaiz = models.ForeignKey('VentaMaiz', on_delete = models.CASCADE)

class Empresa(models.Model):
    ruc = models.CharField(max_length=13,unique=True, blank=False, null=False) 
    razonSocial = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    class Meta:
        verbose_name = 'Productor'
        verbose_name_plural = 'Productores'
        ordering = ['razonSocial']
    
    def __str__(self):
        return self.razonSocial

class VentaMaiz(models.Model):
    fechaVenta = models.DateField()
    observaciones = models.CharField(max_length=100)
    humedad = models.DecimalField(max_digits=4, decimal_places=2)
    impureza = models.DecimalField(max_digits=3, decimal_places=2)
    idEmpresa = models.ForeignKey('Empresa', on_delete = models.CASCADE)
    idBodegaMaiz = models.ForeignKey('BodegaMaiz', on_delete = models.CASCADE)
    idResponsableTransporte = models.ForeignKey('ResponsableTransporte', on_delete = models.CASCADE)

class FacturaVenta(models.Model):
    numeroFactura = models.IntegerField(unique=True)
    fechaEmision = models.DateField()
    cantidad = models.DecimalField(max_digits=7,decimal_places=2)
    preciounitario = models.DecimalField(max_digits=4,decimal_places=2)
    precioTotal = models.DecimalField(max_digits=8,decimal_places=2)
    estado = models.CharField(max_length=25)
    tipoPago = models.CharField(max_length=25)
    idVentaMaiz = models.ForeignKey('VentaMaiz', on_delete = models.CASCADE)
    
class FacturaTransporte(models.Model):
    numerofactura = models.IntegerField()
    fechaFactura = models.DateField()
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    preciounitario = models.DecimalField(max_digits=4,decimal_places=2)
    precioTotal = models.DecimalField(max_digits=8,decimal_places=2)
    estado = models.CharField(max_length=25)
    tipoPago = models.CharField(max_length=25)
    idVentaMaiz = models.ForeignKey('VentaMaiz', on_delete = models.CASCADE)

class Inventario(models.Model):
    id = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length=100, blank = False, null = False)
    cantidad = models.IntegerField(default = 1, blank = False, null = False)
    estado = models.CharField(max_length=25,blank=True, null=True)
    cantidadMin = models.IntegerField(default=2, blank = False, null = False)
    cantidadMax = models.IntegerField(default=10, blank = False, null = False)
    unidadMedida = models.CharField(max_length=100, choices=UNIDAD)
    fechaIngreso = models.DateField(auto_now = True, auto_now_add = False)#models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)
    stock = models.IntegerField(default = 1, blank = False, null = False)   
    idProveedor = models.ForeignKey('Proveedor', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['descripcion']
    
    def __str__(self):
        return self.descripcion

class Articulo(models.Model):
    descripcion = models.CharField(max_length=100)
    estado = models.CharField(max_length=25,blank=True, null=True)
    cantidadMin = models.IntegerField(default=2)
    cantidadMax = models.IntegerField(default=10)
    idProveedor = models.ForeignKey('Proveedor', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'
    
    def __str__(self):
      return self.descripcion

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

class OrdenUso(models.Model):
    cantidad = models.IntegerField()
    unidadMedida = models.CharField(max_length=25)
    fechaSalida = models.DateField()
    idInventario = models.ForeignKey('Inventario', on_delete = models.CASCADE) 
    idEmpleado = models.ForeignKey('Empleado', on_delete = models.CASCADE)

class Empleado(models.Model):
    identificacion = models.CharField(max_length=10,unique=True, blank=False, null=False)
    nombres = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, blank=True, null=True)