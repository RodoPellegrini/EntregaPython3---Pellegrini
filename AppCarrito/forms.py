from django import forms
from .models import Producto, Cliente, Pedido

# para buscar datos
class ProductoBusquedaForm(forms.ModelForm):
    nombre = forms.CharField(required=False)
    categoria = forms.CharField(required=False)

    class Meta:
        model = Producto
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        categoria = cleaned_data.get('categoria')
        if not nombre and not categoria:
            raise forms.ValidationError('Debe ingresar al menos un campo de búsqueda')
        return cleaned_data

class BusquedaForm(forms.Form):
    producto_form = ProductoBusquedaForm()
    


# Para insertar datos

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'




