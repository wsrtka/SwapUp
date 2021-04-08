from django.shortcuts import render
# from django.template import loader
from django.views.generic import View
from django.views import generic
from django.utils import timezone

from django.http import HttpResponseRedirect


# from .forms import UploadFileForm


# Imaginary function to handle an uploaded file.
"""from somewhere import handle_uploaded_file"""


class IndexView(generic.TemplateView):
    template_name = 'exchange/index.html'

def home(request):
    return render(request, 'exchange/index.html')

# def upload_shedule(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         print(form.is_valid())
#         if form.is_valid():
#             #handle_uploaded_file(request.FILES['file'])
#             """
#             def handle_uploaded_file(f):
#                 #przykładowa funkcja handle_uploaded_file
#                 with open('some/file/name.txt', 'wb+') as destination:
#                     for chunk in f.chunks():
#                         destination.write(chunk)
#             """

#             return HttpResponseRedirect('/exchange/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'exchange/upload_shedule.html', {'form': form})

def offers(request):
    return render(request, 'exchange/offers.html')

def manage(request):
    return render(request, 'exchange/manage.html')

def add_offer(request):
    return render(request, 'exchange/add_offer.html')

def add_exchange(request):
    return render(request, 'exchange/add_exchange.html')

def edit_exchange(request):
    return render(request, 'exchange/edit_exchange.html')

def user_offers(request):
    return render(request, 'exchange/user_offers.html')