from django import forms
from django.forms import formset_factory
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from .models import *


class MySelect(forms.Select):
    def render_option(self, selected_choices, option_value, option_label):
        res=""
        if option_value is None:
            option_value = ''
        if option_value =="":
            option_value = "-1"
            res = option_label
            option_label = "cat-white"
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        return format_html('<option value="{0}" class="{2}"{1}>{3}</option>',
                           option_value,
                           selected_html,
                           force_text(option_label),
                           res)

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
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'nombrecat','class':'form-control'}))
    date = forms.DateField(widget=forms.DateInput(format='%m/%d/%Y',attrs={'id': 'datecat','class':'form-control'}), input_formats=('%m/%d/%Y',))
    zoom = forms.FloatField(widget=forms.TextInput(attrs={'id': 'zoom','type': 'hidden', 'value': 14}))
    latitud = forms.FloatField(widget=forms.TextInput(attrs={'id': 'latitud','class':'form-control', 'value' : -33.45}))
    longitud = forms.FloatField(widget=forms.TextInput(attrs={'id': 'longitud','class':'form-control', 'value' : -70.666}))

class CategoryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    style = forms.ModelChoiceField(queryset=Style.objects.all(),empty_label='Seleccione un color', widget=MySelect(attrs={'class':'form-control input-sm','onchange':'changeTest(this)'}))
CategoryFormSet = formset_factory(CategoryForm, extra=1)
