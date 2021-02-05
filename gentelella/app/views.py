from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.template import loader
from django.http import HttpResponse
from app.models import Articulo, Inventario, Productor, Empresa, ResponsableTransporte, PesajeCompraMaiz, CompraMaiz, BodegaMaiz
from app.forms import ProductorForm, InventarioForm, EmpresaForm, ResponsableTransporteForm, CrearProveedorForm, CrearArticuloForm,CrearInventarioForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from app.constants import * #Importar las constantes

MESES = {
    "Enero":"January",
    "Febrero":"February",
    "Marzo":"March",
    "Abril":"April",
    "Mayo":"May",
    "Junio":"June",
    "Julio":"July",
    "Agosto":"August",
    "Septiembre":"September",
    "Octubre":"October",
    "Noviembre":"November",
    "Diciembre":"December"
}

def index(request):
    context = {}
    #template = loader.get_template('app/index.html')pagoCompras.html
    template = loader.get_template('app/pagoCompras.html')
    return HttpResponse(template.render(context, request))

#Paginas de la sección de COMPRAS
def compra_maiz(request, template_name='app/compras/compra_maiz.html'):
    return render(request, template_name)

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

from datetime import date, datetime, timedelta
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder

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

def ingreso_compras(request, template_name='app/compras/ingresarCompras.html'):
    compras = CompraMaiz.objects.filter(valida=True)
    return render(request, template_name, {'compras':compras})

def nuevo_productor(request, template_name='app/compras/nuevoProductor.html'):
    if request.method == 'POST':
        form = ProductorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('compra_m')
    else:
        form = ProductorForm()
    return render(request, template_name,{'form':form})

#Vistas del CRUD de Productor
class CrearProductor(CreateView):
    model = Productor
    template_name = 'app/compras/productor_crear.html'
    form_class = ProductorForm
    success_url = reverse_lazy('listar_productor')

class EditarProductor(UpdateView):
    model = Productor
    form_class = ProductorForm
    template_name = 'app/compras/productor_editar.html'
    success_url = reverse_lazy('listar_productor')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Inventario editado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Hubo problemas para editar esta inventario.')
        return super().form_invalid(form)

class EliminarProductor(DeleteView):
    model = Productor
    template_name = "app/compras/productor_eliminar.html"
    success_url = reverse_lazy('listar_productor')

def listarProductor(request, template_name='app/compras/productor_listar.html'):
    form = Productor.objects.all()
    return render(request, template_name, {'form':form})

#Vistas del CRUD de Empresa
class CrearEmpresa(CreateView):
    model = Empresa
    template_name = 'app/ventas/empresa_crear.html'
    form_class = EmpresaForm
    success_url = reverse_lazy('listar_empresa')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Hubo problemas para crear esta Empresa.')
        return super().form_invalid(form)

class EditarEmpresa(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'app/ventas/empresa_editar.html'
    success_url = reverse_lazy('listar_empresa')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Hubo problemas para editar esta Empresa.')
        return super().form_invalid(form)

class EliminarEmpresa(DeleteView):
    model = Empresa
    template_name = 'app/ventas/empresa_eliminar.html'
    success_url = reverse_lazy('listar_empresa')

def listarEmpresa(request, template_name='app/ventas/empresa_listar.html'):
    form = Empresa.objects.all()
    return render(request, template_name, {'form':form})

def crear_responsable_transporte(request, template_name='app/ventas/transportista_crear.html'):
    if request.method == 'POST':
        responsable_transporteform = CrearResponsableTransporteForm(request.POST)
        if responsable_transporteform.is_valid():
            responsable_transporteform.save()
        return redirect('crear_responsable_transporte')
    else:
        responsable_transporteform = CrearResponsableTransporteForm()
    return render(request, template_name,{'responsable_transporteform':responsable_transporteform})

#Vistas del CRUD de ResponsableTransporte
class CrearResponsableTransporte(CreateView):
    model = ResponsableTransporte
    template_name = 'app/ventas/transportista_crear.html'
    form_class = ResponsableTransporteForm
    success_url = reverse_lazy('listar_responsableTransporte')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Hubo problemas para crear este Responsable de Transporte.')
        return super().form_invalid(form)

class EditarResponsableTransporte(UpdateView):
    model = ResponsableTransporte
    form_class = ResponsableTransporteForm
    template_name = 'app/ventas/transportista_editar.html'
    success_url = reverse_lazy('listar_responsableTransporte')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Hubo problemas para editar este Responsable de Transporte.')
        return super().form_invalid(form)

class EliminarResponsableTransporte(DeleteView):
    model = ResponsableTransporte
    template_name = 'app/ventas/transportista_eliminar.html'
    success_url = reverse_lazy('listar_responsableTransporte')

def listarResponsableTransporte(request, template_name='app/ventas/transportista_listar.html'):
    form = ResponsableTransporte.objects.all()
    return render(request, template_name, {'form':form})

def crear_proveedor(request, template_name='app/inventarios/inventarioIE/proveedor_crear.html'):
    if request.method == 'POST':
        proveedorform = CrearProveedorForm(request.POST)
        if proveedorform.is_valid():
           proveedorform.save()
        return redirect('lista_implementos')
    else:
        proveedorform = CrearProveedorForm()
    return render(request, template_name,{'proveedorform':proveedorform}) 

class CrearArticuloView(CreateView):
    model = Articulo
    template_name = "app/inventarios/inventarioIE/articulo_crear.html"
    form_class = CrearArticuloForm
    success_url = 'lista_implementos'

#views del Inventario
class CrearInventario(CreateView):
    model = Inventario
    template_name = "app/inventarios/inventarioIE/inventario_crear.html"
    form_class = InventarioForm
    success_url = reverse_lazy('listar_inventario')

class ListarInventario(ListView):
    model = Inventario
    template_name = 'app/inventarios/inventarioIE/inventario_listar.html'
    queryset = inventarios = Inventario.objects.all()

class EditarInventario(UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'app/inventarios/inventarioIE/inventario_editar.html'
    success_url = reverse_lazy('lista_implementos')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Inventario editado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Hubo problemas para editar esta inventario.')
        return super().form_invalid(form)

class EliminarInventario(DeleteView):
    model = Inventario
    template_name = "app/inventarios/inventarioIE/inventario_eliminar.html"
    success_url = reverse_lazy('listar_inventario')

def listarVentas(request, template_name='app/inventarios/listar_ventas.html'):
    inventario = Inventario.objects.all()
    return render(request, template_name, {'inventario':inventario})

def convertir_fecha(fecha: str) -> datetime:
    formato_fecha = '%B %d, %Y' # January 28, 2021
    for m in MESES:
        if m == fecha.split(' ')[0]:
            return datetime.strptime(fecha.replace(m, MESES[m]), formato_fecha)            

def reportes_compras(request, template_name='app/inventarios/listar_compras.html'):
    estado = -1 #Por defecto busca todas las compras
    nro_cedula = ''
    
    if request.POST:
        rango_fechas = request.POST['rango_fechas'].split(' - ')
        estado = int(request.POST['estado'])
        nro_cedula = request.POST['nro_cedula']
        
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
    
    if nro_cedula != '': #Si se envía una cédula para buscar
        compras = compras.filter(idProductor__identificacion=nro_cedula)

    return render(request, template_name, {'compras':compras, 'estado':estado, 'nro_cedula':nro_cedula,
        'fechaDesde':fechaDesde, 'fechaHasta':fechaHasta, 'pk_compras':serializers.serialize("json", compras, fields=['pk'])})

def crear_articulo(request, template_name='app/inventarios/inventarioIE/articulo_crear.html'):
    if request.method == 'POST':
        articuloform = CrearArticuloForm(request.POST)
        if articuloform.is_valid():
           articuloform.save()
        return redirect('lista_implementos')
    else:
        articuloform = CrearArticuloForm()
    return render(request, template_name,{'articuloform':articuloform}) 

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path

def imprimir_compras(request):
    pks_input = request.POST['pks_compras'] #pks de la etiqueta input
    pks_compras = pks_input[0:-1].split(' ') #Considerando que llega tipo: '23 '

    for i, value in enumerate(pks_compras): #Convertir pks de 'str' a 'int'
        pks_compras[i]=int(value)
        
    compras = CompraMaiz.objects.filter(pk__in=pks_compras)
    
    #Código necesario para generar el reporte PDF
    template_path = 'app/compras/reporte_pdf.html'
    context = {'compras': compras}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def crear_inventario(request, template_name='app/inventarios/inventarioIE/inventario_crear.html'):
    if request.method == 'POST':
        inventarioform = CrearInventarioForm(request.POST)
        if inventarioform.is_valid():
           inventarioform.save()
        return redirect('lista_implementos')
    else:
        inventarioform = CrearInventarioForm()
    return render(request, template_name,{'inventarioform':inventarioform}) 

def editar_inventario(request,inv):
    #inventario = Inventario.objects.get(id=inv)
    inventario = Inventario.objects.filter(id=inv).first()
    inventarioform = CrearInventarioForm(instance=inventario)
    return render(request,'app/inventarios/inventarioIE/inventario_editar.html', {'inventarioform':inventarioform, 'inventario':inventario} )

def lista_insumos_e_implementos(request, template_name='app/inventarios/inventarioIE/lista_insumos_e_implementos.html'):
    inventario = Inventario.objects.all()
    return render(request, template_name, {'inventario':inventario})
'''
def crear_productor(request, template_name='app/compras/productor_crear.html'):
    if request.method == 'POST':
        form = CrearProductorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('crear_productor')
    else:
        form = CrearProductorForm()
    return render(request, template_name,{'form':form})
'''
def productor_view(request):
    if request.method == 'POST':
        form = ProductorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('compra_m')
    else:
        form = ProductorForm()
    return render(request, 'app/productor_form.html',{'form':form})

#Paginas de la sección Inventarios
def lista_compras(request, template_name='app/inventarios/inventarioCompras.html'):
    return render(request, template_name)

def lista_ventas(request, template_name='app/inventarios/inventarioVentas.html'):
    return render(request, template_name)



def nuevo_proveedor(request, template_name='app/inventarios/nuevoProveedor.html'):
    return render(request, template_name)

def registro_inventario(request, template_name='app/inventarios/registrarInventarioIE.html'):
    return render(request, template_name)

# Paginas de insumos e implementos

def ajuste_inventario(request, template_name='app/inventarios/inventarioIE/ajustarInventarioIE.html'):
    return render(request, template_name)

def ingreso_inventario(request, template_name='app/inventarios/inventarioIE/ingresoInventarioIE.html'):
    return render(request, template_name)

def salida_inventario(request, template_name='app/inventarios/inventarioIE/egresoInventarioIE.html'):
    return render(request, template_name)

def editar_inventario(request, template_name='app/inventarios/inventarioIE/editarInventario.html'):
    return render(request, template_name)


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

