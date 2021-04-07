from django.shortcuts import render
# from django.template import loader
from django.views.generic import View
from django.views import generic
from django.utils import timezone

from django.http import HttpResponseRedirect


from .forms import UploadFileForm


# Imaginary function to handle an uploaded file.
"""from somewhere import handle_uploaded_file"""


# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'exchange/index.html'

# widoki potrzebne do zaimplementowania
# zmienić potem path na odpowiedni plik html
def home(request):
    return render(request, 'exchange/index.html')


def upload_shedule(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            """
            def handle_uploaded_file(f):
                #przykładowa funkcja handle_uploaded_file
                with open('some/file/name.txt', 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            """

            return HttpResponseRedirect('/exchange/')
    else:
        form = UploadFileForm()
    return render(request, 'exchange/upload_shedule.html', {'form': form})

def register():
    return render(request, 'exchange/index.html')

def login():
    return render(request, 'exchange/index.html')