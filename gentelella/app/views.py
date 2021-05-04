from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin#seguridad de login
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import get_template
from django.db.models.functions import Coalesce
from django.db.models import Sum,Count
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from decimal import Decimal
from xhtml2pdf import pisa
from app.models import Articulo,IngresoArticulo,DetalleIngresoArticulos,DetalleSalidaArticulos,SalidaArticulo,Categoria, Inventario, Productor, Empresa, Proveedor, ResponsableTransporte, PesajeCompraMaiz,PesajeVentaMaiz, CompraMaiz, VentaMaiz, BodegaMaiz, Empleado, DocumentoCompra
from app.forms import ProductorForm, InventarioForm, EmpresaForm, ResponsableTransporteForm, ProveedorForm, CrearInventarioForm, ArticuloForm, CategoriaForm, EmpleadoForm,DocumentoCompraForm
from app.utils import * #Importamos métodos útiles
from app.constants import * #Importar las constantes

import json
#import locale
#Idioma "es-ES" (código para el español de España)
#locale.setlocale(locale.LC_ALL, 'es-ES')

#Inicio
#@login_required
#def inicio(request, template_name='app/index2.html'):
#    return render(request, template_name)

#Paginas de la sección de COMPRAS
@login_required
def crear_compra(request, template_name='app/compras/compra_maiz.html'):
    return render(request, template_name)

@login_required
def editar_compra(request, pk, template_name='app/compras/editar_compra_maiz.html'):
    compra = CompraMaiz.objects.get(pk=pk)
    pesajes = PesajeCompraMaiz.objects.filter(idCompraMaiz=pk, vigente=True)
    return render(request, template_name, 
        {'compra':compra, 'pesajes':serializers.serialize("json", pesajes, fields=['fechaPesaje','pesoBruto','pesoTara','pesoNeto','factorConversion','pesoQuintales'])})

@csrf_exempt
def buscar_productor(request):
    cedula = request.POST['nro_cedula']
    productor = Productor.objects.filter(identificacion=cedula)    
    return HttpResponse(serializers.serialize("json", productor), content_type='application/json')

@csrf_exempt
def guardar_pesajes(request):
    formato_fecha = '%d/%m/%Y %H:%M:%S'
    #Datos enviados en la petición AJAX
    pk_productor = int(request.POST['pk_productor'])
    pesajes = json.loads(request.POST['pesajes'])
    total_pesajes = Decimal(request.POST['total_pesajes'])
    observacion = request.POST['observacion']
    
    #Obtener el Productor
    productor = Productor.objects.get(pk=pk_productor)

    #Guardar la Compra de Maíz
    compra_maiz = CompraMaiz(observacion=observacion, humedad=HUMEDAD, 
        impureza=IMPUREZA, total=total_pesajes, idProductor=productor)
    compra_maiz.save()

    #Guardar los Pesajes correspondientes a al Compra de Maíz
    for pes in pesajes:
        fecha = datetime.strptime(pes['fecha'], formato_fecha)
        nuevoPesaje = PesajeCompraMaiz(fechaPesaje=fecha, pesoBruto=int(pes['pesoBruto']),
            pesoTara=int(pes['pesoTara']), pesoNeto=int(pes['pesoNeto']),
            factorConversion=Decimal(pes['factorConversion']), pesoQuintales=Decimal(pes['pesoQuintales']),
            idCompraMaiz=compra_maiz)
        nuevoPesaje.save()
    
    #Guardar registro en Bodega
    bodega_registro =  BodegaMaiz(cantidad=total_pesajes, 
        tipoMovimiento=INGRESO, stockMaiz=total_pesajes, idCompraMaiz=compra_maiz)
    bodega_registro.save()
    
    #return HttpResponse(json.dumps(respuesta, cls=DjangoJSONEncoder), content_type='application/json')
    return HttpResponse('ok')

@csrf_exempt
def editar_pesajes(request):
    formato_fecha = '%d/%m/%Y %H:%M:%S'
    #Datos enviados desde la petición AJAX
    pk_compra = int(request.POST['pk_compra'])
    pes_editar = json.loads(request.POST['pesajes'])
    total_pesajes = Decimal(request.POST['total_pesajes'])
    observacion = request.POST['observacion']

    #Obtener la compra a editar
    compra_maiz = CompraMaiz.objects.get(pk=pk_compra)    
    compra_maiz.observacion = observacion
    compra_maiz.total = total_pesajes
    compra_maiz.save()

    #Anulo los Pesajes anteriores
    pes_anular = PesajeCompraMaiz.objects.filter(idCompraMaiz=pk_compra, vigente=True)
    for pes_anu in pes_anular:
        pes_anu.vigente = False
        pes_anu.save()

    #Guardar los nuevos Pesajes editados correspondientes a al Compra de Maíz
    for pes in pes_editar:
        fecha = datetime.strptime(pes['fechaPesaje'], formato_fecha)
        nuevoPesaje = PesajeCompraMaiz(fechaPesaje=fecha, pesoBruto=int(pes['pesoBruto']),
            pesoTara=int(pes['pesoTara']), pesoNeto=int(pes['pesoNeto']),
            factorConversion=Decimal(pes['factorConversion']), pesoQuintales=Decimal(pes['pesoQuintales']),
            idCompraMaiz=compra_maiz)
        nuevoPesaje.save()
    
    #Guardar registro en Bodega
    bodega_registro =  BodegaMaiz(cantidad=total_pesajes, 
        tipoMovimiento=INGRESO, stockMaiz=total_pesajes, idCompraMaiz=compra_maiz)
    bodega_registro.save()

    #return HttpResponse(json.dumps(respuesta, cls=DjangoJSONEncoder), content_type='application/json')
    return HttpResponse('ok')

@csrf_exempt
def anular_compra(request):
    pk_compra = int(request.POST['pk_compra'])
    compra = CompraMaiz.objects.get(pk=pk_compra)
    compra.valida = False
    compra.save()
        
    return HttpResponse('ok')

@csrf_exempt
def finalizar_compra(request):
    pk_compra = int(request.POST['pk_compra'])
    compra = CompraMaiz.objects.get(pk=pk_compra)
    compra.pendiente = False
    compra.save()
        
    return HttpResponse('ok')

@login_required
def gestion_compras(request, template_name='app/compras/gestion_compras.html'):
    compras = CompraMaiz.objects.filter(valida=True)
    return render(request, template_name, {'compras':compras})

#Vistas del CRUD de Productor
@method_decorator(login_required, name='dispatch')
class CrearProductor(CreateView):
    model = Productor
    template_name = 'app/compras/productor_crear.html'
    form_class = ProductorForm
    success_url = reverse_lazy('listar_productores')

@method_decorator(login_required, name='dispatch')
class EditarProductor(UpdateView):
    model = Productor
    form_class = ProductorForm
    template_name = 'app/compras/productor_editar.html'
    success_url = reverse_lazy('listar_productores')

@method_decorator(login_required, name='dispatch')
class EliminarProductor(DeleteView):
    model = Productor
    template_name = "app/compras/productor_eliminar.html"
    success_url = reverse_lazy('listar_productores')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.Productor.count() > 0:
            messages.add_message(request, messages.ERROR, "Can't be deleted, has childern")
            return redirect('listar_productor')
        return super().delete(request, *args, **kwargs)
        #try:
        #    self.object.delete()
        #    return HttpResponseRedirect(success_url)
        #except ProtectedError:
        #    messages.add_message(request, messages.ERROR, "No se puede eliminar Categoria %s, tiene Articulos vinculados" %self.object.nombre)
       #     return redirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@login_required
def listar_productores(request, template_name='app/compras/productor_listar.html'):
    form = Productor.objects.all()
    return render(request, template_name, {'form':form})

#Vistas del CRUD de Empresa
@method_decorator(login_required, name='dispatch')
class CrearEmpresa(CreateView):
    model = Empresa
    template_name = 'app/ventas/empresa_crear.html'
    form_class = EmpresaForm
    success_url = reverse_lazy('listar_empresas')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Hubo problemas para crear esta Empresa.')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class EditarEmpresa(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'app/ventas/empresa_editar.html'
    success_url = reverse_lazy('listar_empresas')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Hubo problemas para editar esta Empresa.')
        return super().form_invalid(form)


@login_required
def listar_empresas(request, template_name='app/ventas/empresa_listar.html'):
    form = Empresa.objects.all()
    return render(request, template_name, {'form':form})

#Vistas del CRUD de ResponsableTransporte
@method_decorator(login_required, name='dispatch')
class CrearResponsableTransporte(CreateView):
    model = ResponsableTransporte
    template_name = 'app/ventas/transportista_crear.html'
    form_class = ResponsableTransporteForm
    success_url = reverse_lazy('listar_responsableTransporte')

@method_decorator(login_required, name='dispatch')
class EditarResponsableTransporte(UpdateView):
    model = ResponsableTransporte
    form_class = ResponsableTransporteForm
    template_name = 'app/ventas/transportista_editar.html'
    success_url = reverse_lazy('listar_responsableTransporte')

@login_required
def listarResponsableTransporte(request, template_name='app/ventas/transportista_listar.html'):
    form = ResponsableTransporte.objects.all()
    return render(request, template_name, {'form':form})

#PAGINAS DE LA SECCION VENTAS

#Vista de gestion de ventas
@login_required
def gestion_ventas(request, template_name='app/ventas/gestion_ventas.html'):
    ventas = VentaMaiz.objects.filter(valida=True)
    return render(request, template_name, {'ventas':ventas})

#Vista de venta nueva
@login_required
def venta_nueva_maiz(request, template_name='app/ventas/venta_nueva_maiz.html'):
    return render(request, template_name)

@csrf_exempt
def buscar_empresa(request):
    ruc = request.POST['nro_ruc']
    empresa = Empresa.objects.filter(ruc=ruc)    
    return HttpResponse(serializers.serialize("json", empresa), content_type='application/json')

#crear un buscador autocomplete de productor
@csrf_exempt
def buscar_productor_autocomplete(request):    
    data = {}
    try:
        action = request.POST['action']
        if action == 'autocomplete':
            data = []
            prods = Productor.objects.filter(nombres__icontains= request.POST['term'])[0:10]
            for i in prods:
                item = i.toJSON()
                item['text'] = i.nombres
                item['value'] = i.nombres
                data.append(item)  
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)           

#crear un buscador autocomplete de articulo
@csrf_exempt
def buscar_articulo_autocomplete(request):    
    data = {}
    try:
        action = request.POST['action']
        if action == 'autocomplete':
            data = []
            prods = Articulo.objects.filter(descripcion__icontains= request.POST['term'])[0:10]
            for i in prods:
                item = i.toJSON()
                item['text'] = i.descripcion
                data.append(item)  
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)           

#crear un buscador de empresa autocomplete
@csrf_exempt
def buscar_empresa_autocomplete(request):    
    data = {}
    try:
        action = request.POST['action']
        if action == 'autocomplete':
            data = []
            prods = Empresa.objects.filter(razonSocial__icontains= request.POST['term'])[0:10]
            for i in prods:
                item = i.toJSON()
                item['value'] = i.razonSocial 
                data.append(item)  
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)           

#crear un buscador autocomplete de responsable de transporte
@csrf_exempt
def buscar_ResponsableTransporte(request):    
    data = {}
    try:
        action = request.POST['action']
        if action == 'autocomplete':
            data = []
            prods = ResponsableTransporte.objects.filter(nombre__icontains= request.POST['term'])[0:10]
            for i in prods:
                item = i.toJSON()
                item['value'] = i.nombre 
                data.append(item)  
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)           

#crear un buscador de proveedor autocomplete select2
@csrf_exempt
def buscar_proveedor_autocomplete(request):    
    data = {}
    try:
        action = request.POST['action']
        if action == 'autocomplete':
            data = []
            prods = Proveedor.objects.filter(razonSocial__icontains= request.POST['term'])[0:10]
            for i in prods:
                item = i.toJSON()
                item['text'] = i.razonSocial 
                data.append(item)  
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)           

#crear un buscador de empleado autocomplete select2
@csrf_exempt
def buscar_empleado_autocomplete(request):    
    data = {}
    try:
        action = request.POST['action']
        if action == 'autocomplete':
            data = []
            prods = Empleado.objects.filter(nombres__icontains= request.POST['term'])[0:10]
            for i in prods:
                item = i.toJSON()
                item['text'] = i.nombres 
                data.append(item)  
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)

@csrf_exempt
def guardar_pesajes_venta(request):
    formato_fecha = '%d/%m/%Y %H:%M:%S'
    #Datos enviados en la petición AJAX
    pk_empresa = int(request.POST['pk_empresa'])
    pk_responsable_transporte = int(request.POST['pk_responsable_transporte'])
    pesajes = json.loads(request.POST['pesajes'])
    total_pesajes = Decimal(request.POST['total_pesajes'])
    observacion = request.POST['observacion']
    
    #Obtener la empresa
    empresa = Empresa.objects.get(pk=pk_empresa)
    
    #Obtener el Responsable de Transporte
    responsable_transporte= ResponsableTransporte.objects.get(pk=pk_responsable_transporte)

    #Guardar la Compra de Maíz
    venta_maiz = VentaMaiz(observaciones=observacion, humedad=HUMEDAD, 
        impureza=IMPUREZA, total=total_pesajes, idEmpresa=empresa,idResponsableTransporte=responsable_transporte)
    venta_maiz.save()

    #Guardar los Pesajes correspondientes a al Compra de Maíz
    for pes in pesajes:
        fecha = datetime.strptime(pes['fecha'], formato_fecha)
        nuevoPesaje = PesajeVentaMaiz(fechaPesaje=fecha, pesoBruto=int(pes['pesoBruto']),
            pesoTara=int(pes['pesoTara']), pesoNeto=int(pes['pesoNeto']),
            factorConversion=Decimal(pes['factorConversion']), pesoQuintales=Decimal(pes['pesoQuintales']),
            idVentaMaiz=venta_maiz)
        nuevoPesaje.save()
    
    #Guardar registro en Bodega # bodega debemos guardar el ingreso y la salida del mismo
    #bodega_registro =  BodegaMaiz(cantidad=total_pesajes, 
    #    tipoMovimiento=SALIDA, stockMaiz=total_pesajes, idCompraMaiz=compra_maiz)
    #bodega_registro.save()
    
    #return HttpResponse(json.dumps(respuesta, cls=DjangoJSONEncoder), content_type='application/json')
    return HttpResponse('ok')

#editar venta de maiz
@login_required
def editar_venta(request, pk, template_name='app/ventas/editar_venta_maiz.html'):
    venta = VentaMaiz.objects.get(pk=pk)
    pesajes = PesajeVentaMaiz.objects.filter(idVentaMaiz=pk, vigente=True)
    return render(request, template_name, 
        {'venta':venta, 'pesajes':serializers.serialize("json", pesajes, fields=['fechaPesaje','pesoBruto','pesoTara','pesoNeto','factorConversion','pesoQuintales'])})

#editar pesajes de ventas
@csrf_exempt
def editar_pesajes_venta(request):
    formato_fecha = '%d/%m/%Y %H:%M:%S'
    #Datos enviados desde la petición AJAX
    pk_venta = int(request.POST['pk_venta'])
    pes_editar = json.loads(request.POST['pesajes'])
    total_pesajes = Decimal(request.POST['total_pesajes'])
    observacion = request.POST['observacion']

    #Obtener la compra a editar
    venta_maiz = VentaMaiz.objects.get(pk=pk_venta)    
    venta_maiz.observacion = observacion
    venta_maiz.total = total_pesajes
    venta_maiz.save()

    #Anulo los Pesajes anteriores
    pes_anular = PesajeVentaMaiz.objects.filter(idVentaMaiz=pk_venta, vigente=True)
    for pes_anu in pes_anular:
        pes_anu.vigente = False
        pes_anu.save()

    #Guardar los nuevos Pesajes editados correspondientes a al Compra de Maíz
    for pes in pes_editar:
        fecha = datetime.strptime(pes['fechaPesaje'], formato_fecha)
        nuevoPesaje = PesajeVentaMaiz(fechaPesaje=fecha, pesoBruto=int(pes['pesoBruto']),
            pesoTara=int(pes['pesoTara']), pesoNeto=int(pes['pesoNeto']),
            factorConversion=Decimal(pes['factorConversion']), pesoQuintales=Decimal(pes['pesoQuintales']),
            idVentaMaiz=venta_maiz)
        nuevoPesaje.save()
    
    #Guardar registro en Bodega
    #bodega_registro =  BodegaMaiz(cantidad=total_pesajes, 
    #   tipoMovimiento=INGRESO, stockMaiz=total_pesajes, idCompraMaiz=compra_maiz)
    #bodega_registro.save()

    #return HttpResponse(json.dumps(respuesta, cls=DjangoJSONEncoder), content_type='application/json')
    return HttpResponse('ok')

@csrf_exempt
def anular_venta(request):
    pk_venta = int(request.POST['pk_venta'])
    venta = VentaMaiz.objects.get(pk=pk_venta)
    venta.valida = False
    venta.save()
        
    return HttpResponse('ok')

@csrf_exempt
def finalizar_venta(request):
    pk_venta = int(request.POST['pk_venta'])
    venta = VentaMaiz.objects.get(pk=pk_venta)
    venta.pendiente = False
    venta.save()
        
    return HttpResponse('ok')

#Vista de Proveedor
@method_decorator(login_required, name='dispatch')
class CrearProveedor(CreateView):
    model = Proveedor
    template_name = "app/inventarios/proveedor/proveedor_crear.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('listar_proveedor')


@login_required
def listar_proveedor(request, template_name='app/inventarios/proveedor/proveedor_listar.html'):
    form = Proveedor.objects.all()
    return render(request, template_name, {'form':form})

@method_decorator(login_required, name='dispatch')
class EditarProveedor(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'app/inventarios/proveedor/proveedor_editar.html'
    success_url = reverse_lazy('listar_proveedor')

@login_required
def listarVentas(request, template_name='app/inventarios/listar_ventas.html'):
    inventario = Inventario.objects.all()
    return render(request, template_name, {'inventario':inventario})          
  
@login_required
def reportes_compras(request, template_name='app/inventarios/listar_compras.html'):
    
    estado = -1 #Por defecto busca todas las compras
    nom_productor = ''
    
    if request.POST:
        rango_fechas = request.POST['rango_fechas'].split(' - ')
        estado = int(request.POST['estado'])
        nom_productor = request.POST['nom_productor']
        
        fechaDesde = convertir_fecha(rango_fechas[0])
        fechaHasta = convertir_fecha(rango_fechas[1])

    else:
        #Compras de los últimos 7 días
        fechaHasta = date.today() #Hasta hoy
        fechaDesde = fechaHasta - timedelta(days=6) #Desde 6 días atrás        
    
    #"Todas" las compras
    compras = CompraMaiz.objects.filter(valida=True, fechaCompra__range=(fechaDesde, fechaHasta + timedelta(days=1))) #Sumo 1 día ya que no incluye la fechaHasta
    
    if estado != -1: #"Pendiente" o "Finalizada"
        compras = compras.filter(pendiente=bool(estado))
    
    if nom_productor != '': #Si se envía un nombre para buscar
        compras = compras.filter(idProductor__nombres=nom_productor)

    return render(request, template_name, {'compras':compras, 'estado':estado, 'nom_productor':nom_productor,
        'fechaDesde':fechaDesde, 'fechaHasta':fechaHasta, 'pk_compras':serializers.serialize("json", compras, fields=['pk'])})

@login_required
def imprimir_compras(request):
    pks_input = request.POST['pks_compras'] #pks de la etiqueta input
    pks_compras = pks_input[0:-1].split(' ') #Considerando que llega tipo: '23 '

    for i, value in enumerate(pks_compras): #Convertir pks de 'str' a 'int'
        pks_compras[i]=int(value)
        
    compras = CompraMaiz.objects.filter(pk__in=pks_compras)

    date = datetime.now()
    fecha = date    
    fecha1 = date.strftime('%d-%m-%Y-%H-%M')
    
    #Código necesario para generar el reporte PDF
    #template_path = 'app/compras/reporte_pdf.html'
    template_path = 'app/reportes/reporte_compras_pdf.html'
    context = {
        'compras': compras, 
        'reporte' : {'empresa':'Centro de Acopio de Sabanilla',
        'direccion':'Sabanilla-Loja-Ecuador',
        'nombre':'Compras de maíz amarillo duro','fecha':fecha
        }
    }    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte compras %s.pdf"' % (fecha1)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('Tenemos los siguientes errores <pre>' + html + '</pre>')
    return response

@login_required
def reportes_ventas(request, template_name='app/inventarios/listar_ventas_prueba.html'):
    estado = -1 #Por defecto busca todas las ventas 'app/inventarios/listar_ventas.html'
    #nro_ruc = ''
    nom_empresa = ''#agreamos para la busqueda por empresa
    
    if request.POST:
        rango_fechas = request.POST['rango_fechas'].split(' - ')
        estado = int(request.POST['estado'])
        nom_empresa = request.POST['nom_empresa']
        
        fechaDesde = convertir_fecha(rango_fechas[0])
        fechaHasta = convertir_fecha(rango_fechas[1])

    else:
        #Ventas de los últimos 7 días
        fechaHasta = date.today() #Hasta hoy
        fechaDesde = fechaHasta - timedelta(days=6) #Desde 6 días atrás        
    
    #"Todas" las ventas
    ventas = VentaMaiz.objects.filter(valida=True, fechaVenta__range=(fechaDesde, fechaHasta + timedelta(days=1))) #Sumo 1 día ya que no incluye la fechaHasta
    
    if estado != -1: #"Pendiente" o "Finalizada"
        ventas = ventas.filter(pendiente=bool(estado))
    
    #if nro_ruc != '': #Si se envía un ruc para buscar
     #   ventas = ventas.filter(idEmpresa__ruc=nro_ruc)

    if nom_empresa != '': #Si se envia un nombre para buscar
        ventas = ventas.filter(idEmpresa__razonSocial=nom_empresa)

    return render(request, template_name, {'ventas':ventas, 'estado':estado, 'nom_empresa':nom_empresa,
        'fechaDesde':fechaDesde, 'fechaHasta':fechaHasta, 'pk_ventas':serializers.serialize("json", ventas, fields=['pk'])})

@login_required
def imprimir_ventas(request):
    pks_input = request.POST['pks_ventas'] #pks de la etiqueta input
    pks_ventas = pks_input[0:-1].split(' ') #Considerando que llega tipo: '23 '

    for i, value in enumerate(pks_ventas): #Convertir pks de 'str' a 'int'
        pks_ventas[i]=int(value)
        
    ventas = VentaMaiz.objects.filter(pk__in=pks_ventas)

    #fecha = date.strftime('%d/%m/%Y')
    #hora = date.strftime('%H:%M:%S')
    date = datetime.now()
    fecha = date    
    fecha1 = date.strftime('%d-%m-%Y-%H-%M')
    
    #Código necesario para generar el reporte PDF
    #template_path = 'app/compras/reporte_pdf.html'
    template_path = 'app/reportes/reporte_ventas_pdf.html'
    context = {
        'ventas': ventas, 
        'reporte' : {'empresa':'Centro de Acopio de Sabanilla',
        'direccion':'Sabanilla-Loja-Ecuador',
        'nombre':'Ventas de maíz amarillo duro','fecha':fecha
        }
    }
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte venta %s.pdf"' % (fecha1)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def inventario_general(request, template_name='app/inventarios/inventario_general.html'):
    form = Articulo.objects.all()
    return render(request, template_name, {'form':form})

# crear un  articulo
@method_decorator(login_required, name='dispatch')
class CrearArticulo(CreateView):
    model = Articulo
    template_name = 'app/inventarios/articulos/articulo_crear.html'
    form_class = ArticuloForm
    success_url = reverse_lazy('listar_articulo')

@method_decorator(login_required, name='dispatch')
class EditarArticulo(UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'app/inventarios/articulos/articulo_editar.html'
    success_url = reverse_lazy('listar_articulo')

@login_required
def listar_articulo(request, template_name='app/inventarios/articulos/articulo_listar.html'):
    form = Articulo.objects.all()
    return render(request, template_name, {'form':form})

@method_decorator(login_required, name='dispatch')
class CrearCategoria(CreateView):
    model = Categoria
    template_name = 'app/inventarios/categoria/categoria_crear.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('listar_categoria')

@login_required
def listar_categoria(request, template_name='app/inventarios/categoria/categoria_listar.html'):
    form = Categoria.objects.all()
    return render(request, template_name, {'form':form})

@method_decorator(login_required, name='dispatch')
class EditarCategoria(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'app/inventarios/categoria/categoria_editar.html'
    success_url = reverse_lazy('listar_categoria')

from django.db.models import ProtectedError
@method_decorator(login_required, name='dispatch') 
class EliminarCategoria(DeleteView):
    model = Categoria
    template_name = "app/inventarios/categoria/categoria_eliminar.html"
    success_url = reverse_lazy('listar_categoria')    
        #if self.object.count() > 0:
        #   messages.add_message(request, messages.ERROR, "Can't be deleted, has childern")
        #   return redirect('listar_categoria')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            messages.add_message(request, messages.ERROR, "No se puede eliminar Categoria %s, tiene Articulos vinculados" %self.object.nombre)
            return redirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


   
@csrf_exempt
def ingresar_articulo(request, template_name='app/inventarios/articulos/articulo_ingreso.html'):               
   return render(request, template_name)
    
@csrf_exempt
def salida_articulo(request, template_name='app/inventarios/articulos/articulo_salida.html'):                  
    return render(request, template_name)

@csrf_exempt
def guardar_ingreso_articulos(request):
    data = {}
    ingresoArticulos = json.loads(request.POST['ingresoArticulos'])
    ingreso = IngresoArticulo()
    ingreso.idProveedor_id = ingresoArticulos['proveedor']
    ingreso.save()
    for i in ingresoArticulos['articulos']:
        det = DetalleIngresoArticulos()
        det.idArticulo_id = i['id']
        det.cantidad = int(i['cantidad'])
        det.idIngreso_id = ingreso.id
        det.save()
        art = Articulo.objects.get(pk=det.idArticulo_id)
        art.stock =  art.stock + det.cantidad
        art.save()
    data = {'id': ingreso.id}
    #return HttpResponse(json.dumps(respuesta, cls=DjangoJSONEncoder), content_type='application/json')
    return JsonResponse(data, safe=False)

#imprimir pesajes de compra
class ImprimirPesajeCompraPdfView(View):
    def get(self, request, *args, **kwargs):
        try:
            date = datetime.now()
            fecha = date
            fecha1 = date.strftime('%d-%m-%Y-%H-%M')
            template = get_template('app/reportes/reporte_pes_compra_pdf.html')           
            context = {
                    'compra' : CompraMaiz.objects.get(pk=self.kwargs['pk']),
                    'pesajes' : PesajeCompraMaiz.objects.filter(idCompraMaiz=self.kwargs['pk'], vigente=True),                     
                    'reporte' : {
                    'empresa':'Centro de Acopio de Sabanilla',
                    'direccion':'Sabanilla - Loja - Ecuador',
                    'nombre':'Pesajes de compra','fecha':fecha
                    }
                }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="ficha ingreso articulos %s.pdf"' % (fecha1) 
            pisa_status = pisa.CreatePDF(
                    html, dest=response)
            if pisa_status.err:
                return HttpResponse('Existen los siguientes errores <pre>' + html + '</pre>') 
            return response
        except:
            pass
        return response 

#imprimir pesajes de venta
class ImprimirPesajeVentaPdfView(View):
    def get(self, request, *args, **kwargs):
        try:
            date = datetime.now()
            fecha = date
            fecha1 = date.strftime('%d-%m-%Y-%H-%M')
            template = get_template('app/reportes/reporte_pes_venta_pdf.html')           
            context = {
                    'venta' : VentaMaiz.objects.get(pk=self.kwargs['pk']),
                    'pesajes' : PesajeVentaMaiz.objects.filter(idVentaMaiz=self.kwargs['pk'], vigente=True),                     
                    'reporte' : {
                    'empresa':'Centro de Acopio de Sabanilla',
                    'direccion':'Sabanilla - Loja - Ecuador',
                    'nombre':'Pesajes de venta','fecha':fecha
                    }
                }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="ficha pesajes venta %s.pdf"' % (fecha1) 
            pisa_status = pisa.CreatePDF(
                    html, dest=response)
            if pisa_status.err:
                return HttpResponse('Existen los siguientes errores <pre>' + html + '</pre>') 
            return response
        except:
            pass
        return response 

#imprimir inventario en pdf
class ImprimirInventarioPdfView(View):
    def get(self, request, *args, **kwargs):
        try:
            date = datetime.now()
            fecha = date.strftime('%d-%m-%Y %H:%M')   
            fecha1 = date.strftime('%d-%m-%Y-%H-%M')
            template = get_template('app/reportes/reporte_inventario_pdf.html')           
            context = { 
                'inventario': Articulo.objects.all(),
                'reporte' : {
                    'empresa':'Centro de Acopio de Sabanilla',
                    'direccion':'Sabanilla - Loja - Ecuador',
                    'nombre':'Inventario General','fecha':fecha
                    }
                }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Inventario %s.pdf"' % (fecha1) 
            pisa_status = pisa.CreatePDF(
                    html, dest=response)
            if pisa_status.err:
                return HttpResponse('Existen los siguientes errores <pre>' + html + '</pre>') 
            return response
        except:
            pass
        return response 

class ImprimirIngresoPdfView(View):
    def get(self, request, *args, **kwargs):           
        try:
            date = datetime.now()
            fecha = date.strftime("%c")
            template = get_template('app/reportes/reporte_ingreso_art_pdf.html') 
            context = {
                    'ingreso': IngresoArticulo.objects.get(pk=self.kwargs['pk']),
                    'reporte' : {'empresa':'Centro de Acopio de Sabanilla',
                    'direccion':'Sabanilla - Loja - Ecuador',
                    'nombre':'Ingreso de Articulos'}
                    }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="ficha ingreso articulos %s.pdf"' % (fecha)
            pisa_status = pisa.CreatePDF(
                    html, dest=response)
            if pisa_status.err:
                return HttpResponse('Existen los siguientes errores <pre>' + html + '</pre>') 
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('ingresar_articulo'))

class ImprimirSalidaPdfView(View):
    def get(self, request, *args, **kwargs):
        date = datetime.now()
        fecha = date.strftime('%c') 
        try:
            template = get_template('app/reportes/reporte_salida_art_pdf.html') 
            context = {
                    'salida': SalidaArticulo.objects.get(pk=self.kwargs['pk']),
                    'reporte' : {
                        'empresa':'Centro de Acopio de Sabanilla',
                        'direccion':'Sabanilla - Loja - Ecuador',
                        'nombre':'Salida de Articulos',
                        }
                    }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="ficha salida articulos %s.pdf"' % (fecha)
            pisa_status = pisa.CreatePDF(
                    html, dest=response)
            if pisa_status.err:
                return HttpResponse('Existen los siguientes errores <pre>' + html + '</pre>') 
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('ingresar_articulo'))

@csrf_exempt
def guardar_salida_articulos(request):
    data = {}
    salidaArticulos = json.loads(request.POST['salidaArticulos'])
    salida = SalidaArticulo()
    salida.idEmpleado_id = salidaArticulos['empleado']
    salida.save()
    #empleado = salidaArticulos['empleado']
    for i in salidaArticulos['articulos']:
        det = DetalleSalidaArticulos()
        det.idArticulo_id = i['id']
        det.cantidad = int(i['cantidad'])
        det.idSalida_id = salida.id
        det.save()
        art = Articulo.objects.get(pk=det.idArticulo_id)
        art.stock =  art.stock - det.cantidad
        art.save()
    data = {'id': salida.id}
    #return HttpResponse(json.dumps(respuesta, cls=DjangoJSONEncoder), content_type='application/json')
    #return HttpResponse('ok')
    return JsonResponse(data, safe=False)

#Vistas del CRUD de empleado
@method_decorator(login_required, name='dispatch')
class CrearEmpleado(CreateView):
    model = Empleado
    template_name = 'app/inventarios/empleado/empleado_crear.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('listar_empleado')

@login_required
def listar_empleado(request, template_name='app/inventarios/empleado/empleado_listar.html'):
    form = Empleado.objects.all()
    return render(request, template_name, {'form':form})

@method_decorator(login_required, name='dispatch') 
class EditarEmpleado(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'app/inventarios/empleado/empleado_editar.html'
    success_url = reverse_lazy('listar_empleado')

#Pagos
def facturacion_compra(request, template_name='app/pagos/factura_crear_compras.html'):
    #Productores que tienen compras válidas y pendientes
    productores = Productor.objects.filter(pk__in=CompraMaiz.objects.filter(valida=True, pendiente=True).values_list('idProductor'))
    return render(request, template_name, {
        'tiposDocumento': TIPO_DOCUMENTO, 'tiposPago': TIPO_PAGO, 'productores': productores
    })

@csrf_exempt
def obtener_compras_pendientes(request):
    pk_productor = request.POST['pk_productor']
    compras = CompraMaiz.objects.filter(idProductor__pk=pk_productor, valida=True, pendiente=True).values('pk', 'fechaCompra', 'total')
    data=json.dumps(list(compras), cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type='application/json')
    #return HttpResponse(serializers.serialize("json", compras), content_type='application/json')

@csrf_exempt
def guardar_documento(request):
    pk_productor = int(request.POST['pk_productor'])
    pks_compras = json.loads(request.POST['pks_compras'])
    tipo_documento = int(request.POST['tipo_documento']) #código
    nro_documento = int(request.POST['nro_documento'])
    fecha_compra = datetime.strptime(request.POST['fecha_compra'], '%Y-%m-%d')
    cantidad = Decimal(request.POST['cantidad'])
    precio_unitario = Decimal(request.POST['precio_unitario'])
    total = Decimal(request.POST['total'])
    tipo_pago = int(request.POST['tipo_pago']) #código

    productor=Productor.objects.get(pk=pk_productor)

    documento_compra = DocumentoCompra(tipoDocumento=TIPO_DOCUMENTO[tipo_documento],
        numeroDocumento=nro_documento, fechaEmision=fecha_compra, cantidad=cantidad,
        preciounitario=precio_unitario, precioTotal=total, tipoPago=TIPO_PAGO[tipo_pago],
        idProductor=productor)
    
    documento_compra.save()
    
    #Actualizar las compras afectadas
    for pk_compra in pks_compras:
        compra=CompraMaiz.objects.get(pk=pk_compra)
        compra.pendiente = False
        compra.idDocumentoCompra = documento_compra
        compra.save()
    
    return HttpResponse('ok')


@login_required
def CrearDocumentoCompra1(request, template_name='app/pagos/factura_crear_compras.html'):       
    if request.method == 'POST':
        form = DocumentoCompraForm(request.POST)
        action = request.POST['action']
        if action == 'autocomplete':
            data = []
            for i in Productor.objects.filter(nombres__icontains= request.POST['term'])[0:10]:
                item = i.toJSON()
                item['value'] = i.nombres 
                data.append(item)        
        elif action == 'search_productor':
                data = []
                term = request.POST['term']
                clients = Productor.objects.filter(nombres__icontains=term)[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.nombres
                    data.append(item)
        else:
            data['error'] = 'No ha ingresado a ninguna opción'    
        return JsonResponse(data, safe=False)           
        if form.is_valid():
            form.save()
        return redirect('facturacompra1')
        
    else:
        form = DocumentoCompraForm()
    return render(request, template_name,{'form':form})

#vistas de facturacion
@method_decorator(login_required, name='dispatch')  
class CrearDocumentoCompra(CreateView):
    model = DocumentoCompra
    template_name = "app/pagos/factura_crear_compras.html"
    form_class = DocumentoCompraForm
    success_url = 'lista_implementos' 

@csrf_exempt
def buscar_PesajesCompra(request):
    data = {}
    try:
        action = request.POST['action']
        if action == 'buscar_pesaje_compra':
            data = []
            for i in PesajeCompraMaiz.objects.filter(idCompraMaiz_id=1):
                data.append(i.toJSON())
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)

#Pagina del Dashboard 
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'app/dashboard.html'
    #Obtenemos el total de compras
    def get_total_compras(self):
        cant = 0
        try:
            for i in CompraMaiz.objects.all():
              cant += float(i.total)               
        except:
            pass
        return round(cant,2)
    #Obtenemos el total de ventas
    def get_total_ventas(self):
        cant = 0
        try:
            for i in VentaMaiz.objects.all():
               cant += float(i.total )       
        except:
            pass
        return round(cant,2)
    #Obtenemos el numero de productores
    def get_nro_productores(self):
        cant = 0
        try:
            for i in Productor.objects.all():
                cant = cant + 1
        except:
            pass
        return cant
    #Obtenemos el numero de empresas asociadas
    def get_nro_empresas(self):
        cant = 0
        try:
            for i in Empresa.objects.all():
                cant += 1
        except:
            pass
        return cant

    def get_compras_mes(self):
        data = []
       
        try:
            y =  datetime.now().year 
            m =  datetime.now().month
            for m in range(1, 13):
                total = CompraMaiz.objects.filter(fechaCompra__year=y, fechaCompra__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))        
        except:
            pass          
        return data
    
    def get_compras_diario(self):
        data = [] 
        try:
            fechaInicial = datetime.now() - timedelta(days=7) 
            for i in range(1, 8):
                fechaDesde = fechaInicial + timedelta(days=i)
                dia = fechaDesde.day
                mes = fechaDesde.month
                año = fechaDesde.year
                total = CompraMaiz.objects.filter(valida=True, fechaCompra__year=año,fechaCompra__month=mes, fechaCompra__day=dia ).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))   
        except:
            pass
        return data 

    def get_ventas_diario(self):
        data = [] 
        try:
            fechaInicial = datetime.now() - timedelta(days=7) 
            for i in range(1, 8):
                fechaDesde = fechaInicial + timedelta(days=i)
                dia = fechaDesde.day
                mes = fechaDesde.month
                año = fechaDesde.year
                total = VentaMaiz.objects.filter(valida=True, fechaVenta__year=año,fechaVenta__month=mes, fechaVenta__day=dia ).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))   
        except:
            pass
        return data  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_nro_productores'] =  self.get_nro_productores()
        context['get_nro_empresas'] =  self.get_nro_empresas()
        context['get_total_compras'] =  self.get_total_compras()
        context['get_total_ventas'] =  self.get_total_ventas()
        context['get_compras_diario'] =  self.get_compras_diario()
        context['get_ventas_diario'] =  self.get_ventas_diario()      
        return context

def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))
