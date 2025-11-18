from django import forms
from store.models import Categoria, PanelSIP, KitConstruccion, imagenProducto
from .models import Local


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

    # 🔥 ESTA LÍNEA ES LA QUE SOLUCIONA TU PROBLEMA
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = KitConstruccion
        fields = ['nombre', 'precio', 'descripcion', 'm2', 'dormitorios', 'banos', 'categorias']
        

# Formulario de Imagen (ModelForm normal)
class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = imagenProducto
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')

        if imagen:
            # Verificar tipo MIME
            if not imagen.content_type.startswith('image/'):
                raise forms.ValidationError("Solo puedes subir archivos de imagen (JPG, PNG, etc).")

            # Validar tamaño máximo (opcional)
            max_size_mb = 5
            if imagen.size > max_size_mb * 1024 * 1024:
                raise forms.ValidationError(f"La imagen no puede superar los {max_size_mb} MB.")

        return imagen
    

# Formulario Categoría   
class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['nombre', 'ubicacion', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'})
        }