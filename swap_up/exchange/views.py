from django.shortcuts import render
# from django.template import loader
from django.views.generic import View
from django.views import generic


# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'exchange/index.html'

# widoki potrzebne do zaimplementowania
# zmienić potem path na odpowiedni plik html
def home(request):
    return render(request, 'exchange/index.html')

def register():
    return render(request, 'exchange/index.html')

def login():
    return render(request, 'exchange/index.html')