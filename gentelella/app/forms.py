from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin
from django import forms
from app.models import Productor,Empresa,ResponsableTransporte,Proveedor,Articulo,Proveedor,Inventario


class ProductorForm(forms.ModelForm):
    class Meta: 
        model = Productor
        fields = ['identificacion','nombres','direccion','telefono','correo']
        widgets = {
            'identificacion' : forms.TextInput(attrs={'class':'form-control', 'data-inputmask':"'mask' : '9999999999'"}),
            'nombres' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombres y Apellidos completos'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección de domicilio'}),
            'telefono' : forms.TextInput(attrs={'class':'form-control', 'data-inputmask':"'mask' : '9999999999'"}),
            'correo' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'ejemplo@mail.com'})
        }         

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['ruc','razonSocial','direccion','telefono','correo']
        widgets = {
            'ruc' : forms.TextInput(attrs={'class':'form-control', 'data-inputmask':"'mask' : '9999999999999'"}),     
            'razonSocial' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Razón Social / Nombre de la Empresa'}),            
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección de entrega de maíz'}),
            'telefono' : forms.TextInput(attrs={'class':'form-control', 'data-inputmask':"'mask' : '9999999999'"}),
            'correo' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'ejemplo@mail.com'})
        }

class ResponsableTransporteForm(forms.ModelForm):
    class Meta:
        model = ResponsableTransporte
        fields = ['identificacion','nombre','direccion','telefono','correo','placaTrailer']
        widgets = {
            'identificacion' : forms.TextInput(attrs={'class':'form-control', 'data-inputmask':"'mask' : '9999999999'"}),
            'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombres y Apellidos completos'}),           
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección de domicilio'}),
            'telefono' : forms.TextInput(attrs={'class':'form-control', 'data-inputmask':"'mask' : '9999999999'"}),
            'correo' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'ejemplo@mail.com'}),
            'placaTrailer' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Placas del trailer'}),
        }  

class CrearProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['ruc','razonSocial','direccion','telefono','correo']
        widgets = {
            'ruc' : forms.TextInput(attrs={'class':'form-control', 'data-inputmask':"'mask' : '9999999999999'"}),     
            'razonSocial' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Razón Social / Nombre del Proveedor'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección del Proveedor'}),
            'telefono' : forms.TextInput(attrs={'class':'form-control', 'data-inputmask':"'mask' : '9999999999'"}),
            'correo' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'ejemplo@mail.com'})
        }

class CrearInventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['descripcion','cantidad','stock','unidadMedida','estado','cantidadMin','cantidadMax','idProveedor']
        widgets = {
            'descripcion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del Articulo'}),
            'cantidad' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'numero de existencias'}),
            'stock' : forms.NumberInput(attrs={'class':'form-control','readonly': True}),
            'unidadMedida' : forms.Select(attrs={'class':'form-control', 'placeholder':'Elija una opción'}),
            'estado' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba su estado'}),
            'cantidadMin' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'2'}),
            'cantidadMax' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'2'}),
            'idProveedor' : forms.Select(attrs={'class':'form-control', 'placeholder':'Elija una opción'})
        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['descripcion','cantidad','stock','unidadMedida','estado','cantidadMin','cantidadMax','idProveedor']
        widgets = {
            'descripcion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del Articulo'}),
            'cantidad' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'numero de existencias'}),
            'stock' : forms.NumberInput(attrs={'class':'form-control','readonly': True}),
            'unidadMedida' : forms.Select(attrs={'class':'form-control', 'placeholder':'Elija una opción'}),
            'estado' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba su estado'}),
            'cantidadMin' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'2'}),
            'cantidadMax' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'2'}),
            'idProveedor' : forms.Select(attrs={'class':'form-control', 'placeholder':'Elija una opción'})
        }
        

class CrearArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['descripcion','cantidadMin','cantidadMax','idProveedor']
        widgets = {
            'descripcion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del Articulo'}),
            'cantidadMin' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'2'}),
            'cantidadMax' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'2'}),
            'idProveedor' : forms.Select(attrs={'class':'form-control', 'placeholder':'.......'})
        }
        