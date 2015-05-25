from django import forms
from .models import *

class MarkForm(forms.Form):
    description = forms.CharField(widget=forms.TextInput, max_length=100)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Seleccione una categoría", widget=forms.Select(attrs={'class':'form-control input-sm'}))
    latitud = forms.FloatField(widget=forms.TextInput(attrs={'id': 'latitud','type': 'hidden'}))
    longitud = forms.FloatField(widget=forms.TextInput(attrs={'id': 'longitud','type': 'hidden'}))