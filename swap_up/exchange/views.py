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



def import_schedule(csv_file, user):
    
    classes = []
    student = Student.objects.get(user = user)
   
    with io.TextIOWrapper(csv_file, encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:

            subject_name = column[0]
            term_type = column[1]
            term_capacity = column[2]
            group_number = column[3]
            teacher_name = column[4]
            room = column[5]
            week = column[6] 
            day = column[7]
            hour = column[8]

            subject = Subject.objects.get(subject_name = subject_name)
            teacher_first_name, teacher_last_name = teacher_name.split()
            teacher = Teacher.objects.get(first_name = teacher_first_name, last_name = teacher_last_name)

            created_class = Class.objects.create(
                subject_id = subject,
                day = day,
                time = time,
                row = row,
                teacher_id = teacher
            )

            classes.append(created_class)

    for c in classes:
        student.list_of_classes.add(c)


def import_schedule_for_year(csv_file):
    
    semester = 0

    for line in csv_file:
        row = line.decode("utf-8").split(";")

        if len(row) == 1:
            semester = row[0]
        
        else:

            subject_name_row = str(row[0])
            term_type = row[1]
            term_capacity = row[2]
            group_number = row[3]
            teacher_name = row[4]
            room = row[5]
            week = row[6] 
            day = row[7]
            hour = row[8]
            student_name = row[9]

            subject = Subject.objects.create(
                subject_name = subject_name_row,
                category = term_capacity,
                semester = semester
            )


            # teacher_first_name, teacher_last_name = teacher_name.split()
            # student_first_name, student_last_name = student_name.split()

            # test_teacher = Teacher.objects.create(
            #     first_name = 'Jan',
            #     last_name = 'Kowalski'
            # )
            # test_teacher.save()

            # teacher, teacher_created = Teacher.objects.get_or_create(
            #     first_name = teacher_first_name,
            #     last_name = teacher_last_name
            # )
            # if teacher_created:
            #     teacher.save()

            # user = User.objects.get(
            #     first_name = student_first_name,
            #     last_name = student_last_name
            # )
            # if user == None:
            #     print('user is none')

            # student = Student.objects.get(
            #     user = user
            # )

            # # subject = Subject.objects.get(subject_name = subject_name)
            # # teacher = Teacher.objects.get(first_name = teacher_first_name, last_name = teacher_last_name)

            # created_class = Class.objects.create(
            #     subject_id = subject,
            #     day = day,
            #     time = time,
            #     group_number = group_number,
            #     teacher_id = teacher,
            #     capacity = term_capacity,
            #     week = week
            # )

            # created_class.save()
            # student.list_of_classes.add(created_class)
            # student.save()


def upload_csv(request):
    #if request.user
    if request.method == 'POST' and request.FILES['myfile']:

        myfile = request.FILES['myfile']
        for line in myfile:
            print(line)

        import_schedule_for_year(request.FILES['myfile'])

        return render(request, 'exchange/upload_csv.html')

    return render(request, 'exchange/upload_csv.html')



def register():
    return render(request, 'exchange/index.html')

def login():
    return render(request, 'exchange/index.html')

def offers(request):
    return render(request, 'exchange/offers.html')

def manage(request):
    return render(request, 'exchange/manage.html')

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
    return render(request, 'exchange/user_offers.html')
