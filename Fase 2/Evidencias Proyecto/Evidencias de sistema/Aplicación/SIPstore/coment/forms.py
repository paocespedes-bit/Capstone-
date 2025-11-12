from django import forms
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['estrellas', 'comentario']
        widgets = {
            'estrellas': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
