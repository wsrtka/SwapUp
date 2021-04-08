from django.shortcuts import render
# from django.template import loader
from django.views.generic import View
from django.views import generic


# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'exchange/index.html'

def home(request):
    return render(request, 'exchange/index.html')

def offers(request):
    return render(request, 'exchange/offers.html')

def manage(request):
    return render(request, 'exchange/manage.html')