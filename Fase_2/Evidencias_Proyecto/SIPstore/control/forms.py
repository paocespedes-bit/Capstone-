from django import forms
from store.models import Categoria, PanelSIP, KitConstruccion, imagenProducto


# Formulario Categoría
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'})
        }

# Formulario PanelSIP
class PanelSIPForm(forms.ModelForm):
    # Campos de stock que NO son parte directa del modelo PanelSIP
    modo_stock = forms.ChoiceField(
        choices=[('stock', 'Con stock'), ('pedido', 'Por pedido')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Stock'
    )
    cantidad = forms.IntegerField(
        min_value=0,
        required=False, # Puede ser 'Por pedido' y no necesitar cantidad
        label='Cantidad disponible',
        widget=forms.NumberInput(attrs={'class': 'form-control input-cantidad-inventario'})
    )

    class Meta:
        model = PanelSIP
        fields = ['nombre', 'precio', 'descripcion', 'tipo_obs', 'madera_union', 'espesor', 'largo', 'ancho', 'categorias']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_obs': forms.TextInput(attrs={'class': 'form-control'}),
            'madera_union': forms.TextInput(attrs={'class': 'form-control'}),
            'espesor': forms.NumberInput(attrs={'class': 'form-control'}),
            'largo': forms.NumberInput(attrs={'class': 'form-control'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control'}),
            'categorias': forms.CheckboxSelectMultiple()
        }

# Formulario KitConstruccion
class KitConstruccionForm(forms.ModelForm):
    # Campos de stock que NO son parte directa del modelo KitConstruccion
    modo_stock = forms.ChoiceField(
        choices=[('stock', 'Con stock'), ('pedido', 'Por pedido')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Stock'
    )
    cantidad = forms.IntegerField(
        min_value=0,
        required=False,
        label='Cantidad disponible',
        widget=forms.NumberInput(attrs={'class': 'form-control input-cantidad-inventario'})
    )
    
    class Meta:
        model = KitConstruccion
        fields = ['nombre', 'precio', 'descripcion', 'm2', 'dormitorios', 'banos', 'categorias']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'm2': forms.NumberInput(attrs={'class': 'form-control'}),
            'dormitorios': forms.NumberInput(attrs={'class': 'form-control'}),
            'banos': forms.NumberInput(attrs={'class': 'form-control'}),
            'categorias': forms.CheckboxSelectMultiple()
        }

# Formulario de Imagen (ModelForm normal)
class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = imagenProducto
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
