from django.shortcuts import render
# from django.template import loader
from django.views.generic import View
from django.views import generic
from django.utils import timezone

from django.http import HttpResponseRedirect

from .forms import AddExchangeForm


from django.shortcuts import render
  
  



class IndexView(generic.TemplateView):
    template_name = 'exchange/index.html'

def home(request):
    return render(request, 'exchange/index.html')


def import_schedule(csv_file):
    classes = []

    # csv_file = request.FILES[filename]
    data = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data)
    # next(io_string)
    for column in csv.reader(io_string, delimeter = ',', quotechar = "|"):
        subject_name = column[0]
        term_type = column[1]
        term_capacity = column[2]
        group_number = column[3]
        teacher_name = column[4]
        room = column[5]
        # TODO: zajecia co tydzien nie maja tej kolumny, sprawdzac liczbe kolumn
        week = column[6] 
        day = column[7]
        hour = column[8]

        subject = get_subject_by_name(subject_name)
        teacher = get_teacher_by_name(teacher_name)

        
        _, created_class = Class.objects.create(
            subject_id = subject,
            day = day,
            time = time,
            row = row,
            teacher_id = teacher
        )

        classes.append(created_class)

def upload_shedule(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            import_schedule(request.FILES['file'])
            # handle_uploaded_file(request.FILES['file'])
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

def offers(request):
    return render(request, 'exchange/offers.html')

def manage(request):
    return render(request, 'exchange/manage.html')

def add_offer(request):
    return render(request, 'exchange/add_offer.html')

def add_exchange(request):
  

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        form = AddExchangeForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data.get("subject_name"))

            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddExchangeForm()

    context = {
        'form':form
    }


    return render(request, 'exchange/add_exchange.html', context)

def edit_exchange(request):
    return render(request, 'exchange/edit_exchange.html')

def user_offers(request):
    return render(request, 'exchange/user_offers.html')
