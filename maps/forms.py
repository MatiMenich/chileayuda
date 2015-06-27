from django import forms
from .models import *

class MarkForm(forms.Form):
    description = forms.CharField(widget=forms.TextInput, max_length=100)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Seleccione una categoría", widget=forms.Select(attrs={'class':'form-control input-sm','id': 'category-select-list'}))
    latitud = forms.FloatField(widget=forms.TextInput(attrs={'id': 'latitud','type': 'hidden'}))
    longitud = forms.FloatField(widget=forms.TextInput(attrs={'id': 'longitud','type': 'hidden'}))
    idmap = forms.CharField(widget=forms.TextInput(attrs={'id': 'id-map', 'type': 'hidden'}))
"""
    def __init__(self, map, *args, **kwargs):
        super(MarkForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        """