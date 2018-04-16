# Create your views here.
from django.shortcuts import render_to_response
import forms
from django.template import RequestContext

def main_view(request):
    if request.method == 'POST':
        formulario = forms.api_search_form(request.POST)
        if formulario.is_valid():
            user = request.user
            usuario = user.usuario
    else:
        formulario = forms.api_search_form()

    return render_to_response('home.html',{'formulario':formulario}, context_instance=RequestContext(request))