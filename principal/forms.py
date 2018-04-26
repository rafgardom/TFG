# -*- coding: utf-8 -*-
from django import forms
from models import Order, Sort

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')

CONTENT_HELP_TEXT = ' '.join(['<p>Here is some multi-line help',
                              'which is a long string so put',
                              'into a list which is then joined',
                              'with spaces. I can do fun things',
                              'like have <strong>bold</strong>',
                              'and some line breaks.<br/>'])

class api_search_form(forms.Form):
    page = forms.IntegerField(required = False, label='Página', min_value=1)
    pageSize = forms.IntegerField(required=False, label='Tamaño de página', min_value=1)
    order = forms.ModelChoiceField(required=False, queryset=Order.objects.all(), label="Orden por fecha")
    fecha_inicio = forms.DateTimeField(required=False, widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'

                                }), label='Desde')

    fecha_fin = forms.DateTimeField(required=False, widget=forms.TextInput(attrs=
                                {
                                    'class': 'datepicker'
                                }), label='Hasta')
    sort = forms.ModelChoiceField(required=False, queryset=Sort.objects.all(), label="Orden por parámetros")
    q = forms.CharField(required=False, max_length=50, label='Texto libre')
    answers = forms.IntegerField(required = False, label='Número de respuestas', min_value= 1)
    body = forms.CharField(max_length=50, required = False, label='Cuerpo de la pregunta')
    tagged = forms.CharField(max_length=100, required = False, label='Etiquetas')
    title = forms.CharField(max_length=50, required = False, label='Búsqueda por título')