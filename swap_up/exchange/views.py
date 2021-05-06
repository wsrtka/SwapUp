from datetime import datetime

from django.shortcuts import render, redirect
# from django.template import loader
from django.views.generic import View
from django.views import generic
from datetime import date
from django.utils import timezone
import io
import csv
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .service import *


class IndexView(generic.TemplateView):
    template_name = 'exchange/index.html'


def home(request):
    return render(request, 'exchange/index.html')


def import_schedule_for_year(csv_file):
    semester = -1

    for line in csv_file:
        row = line.decode("utf-8").split(";")

        if len(row) == 1:
            semester = row[0]

        elif len(row) == 10:
            subject_name_row = row[0]
            term_type = row[1]

            term_capacity = row[2]
            if term_capacity == '':
                term_capacity = -1

            group_number = row[3]
            if group_number == '':
                group_number = -1

            teacher_name = row[4]
            room = row[5]
            week = row[6]
            day = row[7]
            time = row[8]
            student_index = row[9]

            if subject_name_row != '' and teacher_name != '' and day != '' and time != '':
                subject, created_subject = Subject.objects.get_or_create(
                    subject_name=subject_name_row,
                    category=term_type,
                    semester=semester
                )

                teacher_first_name, teacher_last_name = teacher_name.split()
                # student_first_name, student_last_name = student_name.split()

                teacher, teacher_created = Teacher.objects.get_or_create(
                    first_name=teacher_first_name,
                    last_name=teacher_last_name
                )

                try:
                    # user = User.objects.get(
                    #     first_name=student_first_name,
                    #     last_name=student_last_name
                    # )
                    try:
                        student, created = Student.objects.get_or_create(
                            index_number=student_index,
                            semester=semester
                        )

                        created_class, class_created = Class.objects.get_or_create(
                            subject_id=subject,
                            day=day,
                            time=time,
                            group_number=group_number,
                            teacher_id=teacher,
                            capacity=term_capacity,
                            week=week
                        )
                        if not student.list_of_classes.filter(id=created_class.id).exists():
                            student.list_of_classes.add(created_class)

                    except Student.DoesNotExist:
                        continue

                except User.DoesNotExist:
                    continue


@login_required
def download_schedule(request):
    current_user = request.user
    student = Student.objects.get(user=current_user)
    f = open('schedule.csv', 'w')

    for c in student.list_of_classes.all():
        subject = c.subject_id
        teacher = c.teacher_id
        f.write(
            str(subject.subject_name) + ";" + str(subject.category)
            + ";" + str(c.capacity) + ";" + str(c.group_number) + ";" + str(teacher.first_name) + " " + str(
                teacher.last_name)
            + ";" + str(c.room) + ";" + str(c.week) + ";" + str(c.day) + ";" + str(c.time)
            + "\n"
        )

    f.close()
    f = open('schedule.csv', 'r')
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=schedule.csv'
    return response


@login_required
def upload_csv(request):
    if request.user.is_superuser:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            import_schedule_for_year(request.FILES['myfile'])

            return render(request, 'exchange/upload_csv.html')

        return render(request, 'exchange/upload_csv.html')
    else:
        return render(request, 'base.html')


@login_required
def exhange(request, exchange_id):
    name = ''
    items = []
    db_exchanges = Exchange.objects.all()
    for exchange in db_exchanges:
        if exchange.semester == exchange_id:
            name = exchange.name

    db_offers = Offer.objects.all()

    for offer in db_offers:
        # if offer.exchange and offer.exchange.semester == exchange_id:
        item_dict = {
            "student": f'{offer.student.user.first_name} {offer.student.user.last_name}' if offer.student.user.first_name and offer.student.user.last_name else 'Anonymous',
            "subject": offer.unwanted_class.subject_id.subject_name if offer.unwanted_class.subject_id.subject_name else '',
            "time": f'{offer.unwanted_class.day} {offer.unwanted_class.week} | {offer.unwanted_class.time}' if offer.unwanted_class else '',
            "other_times": offer.preferred_days,
            "teacher": f'{offer.unwanted_class.teacher_id.first_name} {offer.unwanted_class.teacher_id.last_name}' if offer.unwanted_class.teacher_id else '',
            "other_teachers": ",".join([f'{teacher.first_name} {teacher.last_name}' for teacher in offer.preferred_teachers.all()]),
            "comment": offer.additional_information if offer.additional_information else None,
        }
        items.append(item_dict)

    if request.GET.get('delete_offer'):
        print(request.GET.get('delete_offer'))
        # Offer.objects.exchange.filter(id=int(request.GET.get('delete_offer'))).delete()
        # return redirect(str(exchange_id))

    return render(request, 'exchange/exchange.html', {'items': items, 'name': name})


@login_required
def manage(request):
    Exchange.objects.all().delete()
    for i in range(1, 11):
        exchange = Exchange.objects.create(
            name="Semester " + str(i),
            semester=i
        )
    if request.user.is_superuser:
        db_exchanges = Exchange.objects.all()
        exchanges = []
        for exchange in db_exchanges:
            exchange_dict = {
                "name": exchange.name,
                "id": exchange.semester
            }

            exchanges.append(exchange_dict)

        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            import_schedule_for_year(request.FILES['myfile'])

            return render(request, 'exchange/manage.html', {'exchanges': exchanges})

        if request.GET.get('delete_exchange'):
            if request.GET.get('delete_exchange') != '':
                # print(request.GET.get('delete_exchange'))
                # Exchange.objects.filter(semester=int(request.GET.get('delete_exchange'))).delete()
                db_offers = Offer.objects.all()
                db_offers = [offer for offer in db_offers if offer.exchange is not None and offer.exchange.semester == int(request.GET.get('delete_exchange'))]
                for offer in db_offers:
                    offer.delete()
                return redirect('manage')

        return render(request, 'exchange/manage.html', {'exchanges': exchanges})
    else:
        return render(request, 'base.html')


@login_required
def offers(request):
    current_student = request.user.student
    db_offers = Offer.objects.filter(state=('N', 'New')).exclude(student_id=current_student.id)
    # db_offers = [offer for offer in db_offers if offer.exchange.semester == current_student.semester]

    offers = []

    # niestety tak jest najwygodniej przekazać parametry do kontekstu template'a
    for offer in db_offers:
        offer_dict = {}
        offer_dict[
            'student'] = f'{offer.student.user.first_name} {offer.student.user.last_name}' if offer.student.user.first_name and offer.student.user.last_name else 'Anonymous'
        offer_dict[
            'subject'] = offer.unwanted_class.subject_id.subject_name if offer.unwanted_class.subject_id.subject_name else ''
        offer_dict[
            'time'] = f'{offer.unwanted_class.day} {offer.unwanted_class.week}, {offer.unwanted_class.time}' if offer.unwanted_class else ''
        offer_dict[
            'teacher'] = f'{offer.unwanted_class.teacher_id.first_name} {offer.unwanted_class.teacher_id.last_name}' if offer.unwanted_class.teacher_id else ''
        offer_dict['comment'] = offer.additional_information if offer.additional_information else None
        offer_dict['preferred_days'] = offer.preferred_days
        offer_dict['preferred_hours'] = offer.preferred_times
        offer_dict['preferred_teachers'] = [f'{teacher.first_name} {teacher.last_name}' for teacher in
                                            offer.preferred_teachers.all()]

        offers.append(offer_dict)

    offers1 = offers[::2]
    offers2 = offers[1::2]

    return render(request, 'exchange/offers.html', {'offers1': offers1, 'offers2': offers2})


@login_required
def add_exchange(request):
    if request.method == 'POST':
        form = AddExchangeForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            exchange = Exchange.objects.create(
                name=form_data['name'],
                semester=form_data['semester']
            )

            return HttpResponseRedirect('/exchange/manage')

    else:
        form = AddExchangeForm()

    context = {
        'form': form
    }

    return render(request, 'exchange/add_exchange.html', context)


@login_required
def add_offer(request):
    if request.method == 'POST' and 'schedule_button' in request.POST:
        class_id = request.POST['schedule_button']
        unwanted_class = Class.objects.get(id=class_id)
        subject = unwanted_class.subject_id
        print(subject.subject_name)

        all_classes = Class.objects.filter(subject_id=subject)
        # Tutaj dla tych wszystkich przedmiotów wyliczam dane do wyświetlenia
        print(all_classes)

        schedule = {
            'Pn': [], 'Wt': [], 'Śr': [], 'Czw': [], 'Pt': []
        }

        week = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']

        context = {}

        for c in all_classes:
            class_dict = create_class_dict(c)
            count_collisions(c, class_dict, schedule)

        arrange_horizontal_position(schedule)

        context_schedule = [{'schedule': schedule['Pn'], 'name': 'Poniedziałek'},
                            {'schedule': schedule['Wt'], 'name': 'Wtorek'},
                            {'schedule': schedule['Śr'], 'name': 'Środa'},
                            {'schedule': schedule['Czw'], 'name': 'Czwartek'},
                            {'schedule': schedule['Pt'], 'name': 'Piątek'}
                            ]

        return render(request, 'exchange/add_offer_new.html', {'schedule': context_schedule, 'subject_name': subject.subject_name})

    elif request.method == 'POST':
        print(request.POST['yellow'])
        print(request.POST['green'])
        print(request.POST['comment'])

    return HttpResponseRedirect('/exchange/my-offers')


@login_required
def add_offer_old(request):
    if request.method == 'POST':
        if 'schedule_button' in request.POST:
            class_id = request.POST['schedule_button']
            unwanted_class = Class.objects.get(id=class_id)
            subject = unwanted_class.subject_id
            print(subject.subject_name)

        form = AddOfferForm(request.POST, user=request.user)

        if form.is_valid():

            # pobranie danych z formularza
            form_data = form.cleaned_data
            try:
                unwanted_class = Class.objects.get(
                    subject_id=Subject.objects.get(subject_name=form_data['subject_name']),
                    teacher_id=Teacher.objects.get(last_name=form_data['teacher']),
                    day=form_data['have_day_of_the_week'],
                    time=form_data['have_time']
                )
            except Class.DoesNotExist:
                messages.error(request, 'Invalid class: you are trying to exchange a class that does not exist!')

                context = {
                    'form': form
                }

                return render(request, 'exchange/add_offer.html', context)

            # tworzenie nowej oferty w BD i ustawianie jej atrybutów
            offer = Offer.objects.create(
                student=request.user.student,
                exchange=Exchange.objects.get(semester=request.user.student.semester),
                unwanted_class=unwanted_class,
                additional_information=form_data['comment']
            )

            offer.preferred_days = form_data['want_day']
            offer.preferred_times = form_data['want_time']

            teachers = []

            for teacher in form_data['preferred_teachers']:
                teachers.append(Teacher.objects.get(last_name=teacher))

            # ten atrybut może powstać dopiero po tym, jak stworzony zostanie obiekt Offer
            offer.preferred_teachers.set(teachers)

            return HttpResponseRedirect('/exchange/my-offers')

    else:
        form = AddOfferForm(user=request.user)

    context = {
        'form': form
    }

    return render(request, 'exchange/add_offer.html', context)


@login_required
def edit_exchange(request):
    return render(request, 'exchange/edit_exchange.html')


@login_required
def user_offers(request):
    offer1 = {
        "subject": "Teoria nicości2",
        "have_time": "Pn A, 8:00",
        "have_teacher": "Zenon Iksiński",
        "state": "new",
        "other_student": None,
        "other_time": None,
        "other_teacher": None
    }

    offer2 = {
        "subject": "Teoria nicości",
        "have_time": "Pn A, 8:00",
        "have_teacher": "Zenon Iksiński",
        "state": "pending",
        "other_student": "Staszek Ciaptak-Gąsiennica",
        "other_time": "Wt B, 9:35",
        "other_teacher": None
    }

    offer3 = {
        "subject": "Wprowadzenie do teorii nicości",
        "have_time": "Pn A, 8:00",
        "have_teacher": "Zenon Iksiński",
        "state": "closed",
        "other_student": "Józio Chmura-Mamałyga",
        "other_time": "Wt B, 9:35",
        "other_teacher": None
    }

    # static offers
    # offers = [offer1, offer2, offer3]

    # dynamic offers
    current_student = request.user.student
    db_offers = Offer.objects.filter(student_id=current_student.id)

    offers = []

    # niestety tak jest najwygodniej przekazać parametry do kontekstu template'a
    for offer in db_offers:
        offer_dict = {}
        offer_dict[
            'subject'] = offer.unwanted_class.subject_id.subject_name if offer.unwanted_class.subject_id.subject_name else ''
        offer_dict[
            'have_time'] = f'{offer.unwanted_class.day} {offer.unwanted_class.week}, {offer.unwanted_class.time}' if offer.unwanted_class else ''
        offer_dict[
            'have_teacher'] = f'{offer.unwanted_class.teacher_id.first_name} {offer.unwanted_class.teacher_id.last_name}' if offer.unwanted_class.teacher_id else ''
        offer_dict['state'] = offer.state.split('\'')[3] if offer.state else ''
        offer_dict[
            'other_student'] = f'{offer.other_student.user.first_name} {offer.other_student.user.last_name}' if offer.other_student else ''
        offer_dict['other_time'] = ''
        offer_dict['other_teacher'] = ''

        offers.append(offer_dict)

    return render(request, 'exchange/user_offers.html', {'offers': offers})


@login_required
def schedule(request):
    current_user = request.user
    student = Student.objects.get(user=current_user)

    schedule = {
        'Pn': [], 'Wt': [], 'Śr': [], 'Czw': [], 'Pt': []
    }

    week = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']

    context = {}

    for c in student.list_of_classes.all():
        class_dict = create_class_dict(c)
        count_collisions(c, class_dict, schedule)

    arrange_horizontal_position(schedule)

    context = [{'schedule': schedule['Pn'], 'name': 'Poniedziałek'},
               {'schedule': schedule['Wt'], 'name': 'Wtorek'},
               {'schedule': schedule['Śr'], 'name': 'Środa'},
               {'schedule': schedule['Czw'], 'name': 'Czwartek'},
               {'schedule': schedule['Pt'], 'name': 'Piątek'}
               ]

    return render(request, 'exchange/schedule.html', {'context': context})


def dashboard(request):
    latest_offers = Offer.objects.all().exclude(student=request.user.student)

    if len(latest_offers) > 3:
        latest_offers = latest_offers[:3]

    user_offers = Offer.objects.all().filter(student=request.user.student)

    if len(user_offers) > 3:
        user_offers = user_offers[:3]

    l_offers = []
    u_offers = []

    for offer in latest_offers:
        offer_dict = {}
        offer_dict['subject'] = offer.unwanted_class.subject_id.subject_name if offer.unwanted_class.subject_id.subject_name else ''
        offer_dict['have_time'] = f'{offer.unwanted_class.day} {offer.unwanted_class.week}, {offer.unwanted_class.time}' if offer.unwanted_class else ''
        offer_dict['have_teacher'] = f'{offer.unwanted_class.teacher_id.first_name} {offer.unwanted_class.teacher_id.last_name}' if offer.unwanted_class.teacher_id else ''
        offer_dict['state'] = offer.state.split('\'')[3] if offer.state else ''
        offer_dict['other_student'] = f'{offer.other_student.user.first_name} {offer.other_student.user.last_name}' if offer.other_student else ''
        offer_dict['other_time'] = ''
        offer_dict['other_teacher'] = ''

        l_offers.append(offer_dict)

    for offer in user_offers:
        offer_dict = {}
        offer_dict['subject'] = offer.unwanted_class.subject_id.subject_name if offer.unwanted_class.subject_id.subject_name else ''
        offer_dict['have_time'] = f'{offer.unwanted_class.day} {offer.unwanted_class.week}, {offer.unwanted_class.time}' if offer.unwanted_class else ''
        offer_dict['have_teacher'] = f'{offer.unwanted_class.teacher_id.first_name} {offer.unwanted_class.teacher_id.last_name}' if offer.unwanted_class.teacher_id else ''
        offer_dict['state'] = offer.state.split('\'')[3] if offer.state else ''
        offer_dict['other_student'] = f'{offer.other_student.user.first_name} {offer.other_student.user.last_name}' if offer.other_student else ''
        offer_dict['other_time'] = ''
        offer_dict['other_teacher'] = ''

        u_offers.append(offer_dict)

    return render(request, 'exchange/dashboard.html', {"l_offers": l_offers, "u_offers": u_offers})
