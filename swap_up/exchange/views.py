from django.shortcuts import render
# from django.template import loader
from django.views.generic import View
from django.views import generic


# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'exchange/index.html'

# widoki potrzebne do zaimplementowania
def register():
    pass

def login():
    pass

def home():
    pass