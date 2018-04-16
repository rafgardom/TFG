# -*- coding: utf-8 -*-
from django import forms
from models import Order, Sort
import datetime

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')

class api_search_form(forms.Form):
    page = forms.IntegerField(required = False, label='Páginas')
    pageSize = forms.IntegerField(required=True, label='Tamaño de página')
    order = forms.ModelChoiceField(queryset=Order.objects.all(), label="Orden por fecha")
    fecha_inicio = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }), label='Desde')

    fecha_fin = forms.DateField(widget=forms.TextInput(attrs=
    {
        'class': 'datepicker'
    }), label='Hasta')
    sort = forms.ModelChoiceField(queryset=Sort.objects.all(), label="Orden por parámetros")
    q = forms.CharField(max_length=50, required = True, label='Texto libre')
    answers = forms.IntegerField(required = False, label='Número de respuestas')
    body = forms.CharField(max_length=50, required = True, label='Cuerpo de la pregunta')
    tagged = forms.CharField(max_length=100, required = True, label='Etiquetas contenidas (separar por ";")')
    title = forms.CharField(max_length=50, required = True, label='Búsqueda por título')