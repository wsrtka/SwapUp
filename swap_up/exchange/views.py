from django.shortcuts import render
# from django.template import loader
from django.views.generic import View
from django.views import generic
from django.utils import timezone
import io
import csv
from django.http import HttpResponseRedirect

from .forms import AddExchangeForm, UploadFileForm


from django.shortcuts import render
from .models import *


class IndexView(generic.TemplateView):
    template_name = 'exchange/index.html'

def home(request):
    return render(request, 'exchange/index.html')


def import_schedule_for_year(csv_file):
    
    semester = 0

    for line in csv_file:
        row = line.decode("utf-8").split(";")

        if len(row) == 1:
            semester = row[0]
        
        else:

            subject_name_row = row[0]
            term_type = row[1]
            term_capacity = row[2]
            group_number = row[3]
            teacher_name = row[4]
            room = row[5]
            week = row[6] 
            day = row[7]
            time = row[8]
            student_name = row[9]

            subject, created_subject = Subject.objects.get_or_create(
                subject_name = subject_name_row,
                category = term_capacity,
                semester = semester
            )

            teacher_first_name, teacher_last_name = teacher_name.split()
            student_first_name, student_last_name = student_name.split()

            teacher, teacher_created = Teacher.objects.get_or_create(
                first_name = teacher_first_name,
                last_name = teacher_last_name
            )

            user = User.objects.get(
                first_name = student_first_name,
                last_name = student_last_name
            )

            student = Student.objects.get(
                user = user
            )

            created_class = Class.objects.create(
                subject_id = subject,
                day = day,
                time = time,
                group_number = group_number,
                teacher_id = teacher,
                capacity = term_capacity,
                week = week
            )

            student.list_of_classes.add(created_class)



def download_schedule(request):
    current_user = request.user
    student = Student.objects.get(user = user)
    f = open('schedule.csv', 'wb')
    for c in student.list_of_classes:
        subject_id = c.subject_id
        subject = Subject.objects.get(id = subject_id)
        teacher_id = c.teacher_id
        teacher = Teacher.objects.get(id = teacher_id)
        f.write(
            subject.subject_name + ";" + subject.category
            + ";" + c.capacity + ";" + c.group_number + ";" + teacher.first_name + " " + teacher.last_name
            + ";" + c.room + ";" + c.week + ";" + c.day + ";" + c.time
            + "\n"
        )

    f.close()
    f = open('schedule.csv', 'r')
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=schedule.csv'
    return response
        


def upload_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:

        myfile = request.FILES['myfile']
        # for line in myfile:
        #     print(line)

        import_schedule_for_year(request.FILES['myfile'])

        return render(request, 'exchange/upload_csv.html')

    return render(request, 'exchange/upload_csv.html')


def exhange(request, exchange_id):

    # TODO
    item1 = {
        "student": "Jacek Gorm",
        "subject": "Teoria nicości2",
        "time": "Pn A, 8:00",
        "other_times": "Pn B, 9:00, Wt B, 16:15", #none means any class
        "teacher": "Zenon Iksiński",
        "other_teachers": None, #none means any teacher
        "comment": None,
    }
    item2 = {
        "student": "Jacek Gorm",
        "subject": "WDI",
        "time": "Śr, 10:00",
        "other_times": "Pn B, 9:00, Wt B, 16:15",
        "teacher": "Zenon Iksiński",
        "other_teachers": "Ikakij Korek",
        "comment": "daję 100zł",
    }
    item3 = {
        "student": "Jacek Gorm",
        "subject": "Analiza",
        "time": "Pn B, 8:00",
        "other_times": None,
        "teacher": "Zenon Iksiński",
        "other_teachers": "Ikakij Korek, Szymon Tukor",
        "comment": "daję 100zł",
    }
    exchange1 = {
        "name": "Semester 1",
        "id" : 1,
        "items": [item1, item2],
    }
    exchange2 = {
        "name": "Semester 2",
        "id": 2,
        "items": [item1, item2, item3],
    }
    exchange3 = {
        "name": "Semester 3",
        "id": 3,
        "items": [item1],
    }
    exchange4 = {
        "name": "Semester 4",
        "id": 4,
        "items": [item1, item1],
    }
    exchange5 = {
        "name": "Semester 5",
        "id": 5,
        "items": [item2],
    }
    items = []
    name = ''
    exchanges = [exchange1, exchange2, exchange3, exchange4, exchange5]
    for exchange in exchanges:
        if exchange["id"] == exchange_id:
            items = exchange["items"]
            name = exchange["name"]

    return render(request, 'exchange/exchange.html', {'items': items, 'name': name})


def register(request):
    return render(request, 'exchange/index.html')

def login(request):
    return render(request, 'exchange/index.html')

def offers(request):
    return render(request, 'exchange/offers.html')

def manage(request):
    exchange1 = {
        "name": "Semester 1",
        "id": "1",
    }
    exchange2 = {
        "name": "Semester 2",
        "id": "2",
    }
    exchange3 = {
        "name": "Semester 3",
        "id": "3",
    }
    exchange4 = {
        "name": "Semester 4",
        "id": "4",
    }
    exchange5 = {
        "name": "Semester 5",
        "id": "5",
    }
    exchanges = [exchange1, exchange2, exchange3, exchange4, exchange5]

    return render(request, 'exchange/manage.html', {'exchanges': exchanges})

def add_exchange(request):
    return render(request, 'exchange/add_exchange.html')

def add_offer(request):
  

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


    return render(request, 'exchange/add_offer.html', context)

def edit_exchange(request):
    return render(request, 'exchange/edit_exchange.html')

def user_offers(request):
    #TODO Te słowniki można by tworzyć w tym miesjcu na podstawie bazy
    # I podawać poprawne zamiast tych przykładowych

    offer1 = {
        "subject": "Teoria nicości2",
        "have_time": "Pn A, 8:00",
        "have_teacher": "Zenon Iksiński",
        "state" : "new",
        "other_student": None,
        "other_time": None,
        "other_teacher": None
    }

    offer2 = {
        "subject": "Teoria nicości",
        "have_time": "Pn A, 8:00",
        "have_teacher": "Zenon Iksiński",
        "state" : "pending",
        "other_student": "Staszek Ciaptak-Gąsiennica",
        "other_time": "Wt B, 9:35",
        "other_teacher": None
    }

    offer3 = {
        "subject": "Wprowadzenie do teorii nicości",
        "have_time": "Pn A, 8:00",
        "have_teacher": "Zenon Iksiński",
        "state" : "closed",
        "other_student": "Józio Chmura-Mamałyga",
        "other_time": "Wt B, 9:35",
        "other_teacher": None
    }

    # static offers
    # offers = [offer1, offer2, offer3]
    
    # dynamic offers
    current_student = request.user.student
    offers = Offer.objects.filter(student_id=current_student.id)

    return render(request, 'exchange/user_offers.html', {'offers': offers})


def schedule(request):
    #Todo

    Pn = [
        {'start': 8.00, 'end': 9.35, 'subject': "Analiza", 'week':None, 'teacher':"Zenon Iksiński"},
        {'start': 9.35, 'end': 11.15, 'subject': "Analiza", 'week':None, 'teacher':"Zenon Iksiński"},
        {'start': 14.40, 'end': 16.10, 'subject': "Analiza", 'week':None, 'teacher':"Zenon Iksiński"},
    ]
    return render(request, 'exchange/shedule.html', {'Pn':pn, 'Wt':wt, 'Śr':sr, 'Czw':czw, 'Pt':pt, 'Sb':sb, 'Nd':nd})