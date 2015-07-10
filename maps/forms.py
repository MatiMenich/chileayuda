from django import forms
from django.forms import formset_factory
from .models import *


class MySelect(forms.Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return u'<option class=\"'+str(option_label)+'\"> </option>'

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

class WizardForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, max_length=100)
    latitud = forms.FloatField(widget=forms.TextInput(attrs={'id': 'latitud','type': 'hidden'}))
    longitud = forms.FloatField(widget=forms.TextInput(attrs={'id': 'longitud','type': 'hidden'}))
    description = forms.CharField(widget=forms.TextInput, max_length=100)

class CategoryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, max_length=100)
    style = forms.ModelChoiceField(queryset=Style.objects.all(), empty_label="Seleccione un color", widget=MySelect(attrs={'class':'form-control input-sm'}))
CategoryFormSet = formset_factory(CategoryForm, extra=1)


