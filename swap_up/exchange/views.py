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
from django.core.mail import send_mail


def send_offer_accept_mail(user):
    send_mail(
        subject='[SwapUp] Status of your offer changed',
        message='Someone has just accepted one of your offers! Visit http://wsrtk.pythonanywhere.com/exchange/my-offers to see what\'s going on. \n\n \
            If you don\'t want to receive notification emails, please go to your profile and change the appropriate option.',
        from_email='swap.up.io.2021@gmail.com',
        recipient_list=[user.email],
        fail_silently=True
    )


def send_swap_accept_mail(user):
    send_mail(
        subject='[SwapUp] Status of your offer changed',
        message='Someone has just confirmed your swap! Visit http://wsrtk.pythonanywhere.com/exchange/schedule/ to see your new schedule. \n\n \
            If you don\'t want to receive notification emails, please go to your profile and change the appropriate option.',
        from_email='swap.up.io.2021@gmail.com',
        recipient_list=[user.email],
        fail_silently=True
    )

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
                    name=subject_name_row,
                    category=term_type,
                    semester=semester
                )

                # student_first_name, student_last_name = student_name.split()

                teacher, teacher_created = Teacher.objects.get_or_create(
                    name=teacher_name
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
                            subject=subject,
                            day=day,
                            time=time,
                            group_number=group_number,
                            teacher=teacher,
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
        subject = c.subject
        teacher = c.teacher
        f.write(
            str(subject.name) + ";" + str(subject.category)
            + ";" + str(c.capacity) + ";" + str(c.group_number) + ";" + str(teacher.name)
            + ";" + str(c.room) + ";" + str(c.week) + ";" + str(c.day) + ";" + str(c.time)
            + "\n"
        )

    f.close()
    f = open('schedule.csv', 'r')
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=schedule.csv'
    return response


def get_classes_student_list(clss):
    students = []

    for student in Student.objects.all():
        if clss in student.list_of_classes.all():
            students.append(student)

    return students


def get_classes_free_spots(clss):
    if clss.capacity != None:
        taken_spots = len(get_classes_student_list(clss))
        return (clss.capacity - taken_spots)
    else:
        return 0


@login_required
def download_subject_student_list(request):
    try:
        subjects = []
        semester_id = request.user.student.semester
        subjects = Subject.objects.filter(semester=semester_id)
        print("Semester " + str(semester_id))

    except Student.DoesNotExist:
        subjects = Subject.objects.all()

    return render(request, 'exchange/download_subject.html', {'subjects': subjects})


@login_required
def download_certain_subject_student_list(request, subject_id):
    if request.user.is_superuser:

        subject = Subject.objects.get(id=subject_id)
        classes = Class.objects.filter(subject_id=subject_id)

        filename = subject.name + "list.csv"
        f = open(filename, 'w')
        f.write(subject.name + "\n")

        for clss in classes:

            teacher = clss.teacher
            students = get_classes_student_list(clss)

            for student in students:
                f.write(str(clss.group_number) + ";"
                        + str(clss.day) + ";"
                        + str(clss.time) + ";"
                        + str(teacher.name) + ";"
                        + str(student.index_number)
                        + "\n"
                        )

        f.close()
        f = open(filename, 'r')
        response = HttpResponse(f, content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename= "' + filename + '"'
        response['Content-Disposition'] = 'attachment; filename=list.csv'

        return response
    else:
        return render(request, 'base.html')


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
def exchange(request, exchange_id):
    name = ''
    items = []
    db_exchanges = Exchange.objects.all()
    for exchange in db_exchanges:
        if exchange.semester == exchange_id:
            name = exchange.name
            semester = exchange.semester

    db_offers = Offer.objects.all()
    for offer in db_offers:
        if offer.exchange and offer.exchange.semester == exchange_id:
            item_dict = {
                "id": f'{offer.id}',
                "student": f'{offer.student.user.first_name} {offer.student.user.last_name}' if offer.student.user.first_name and offer.student.user.last_name else 'Anonymous',
                "subject": offer.unwanted_class.subject.name if offer.unwanted_class.subject.name else '',
                "time": f'{offer.unwanted_class.day} {offer.unwanted_class.week} | {offer.unwanted_class.time}' if offer.unwanted_class else '',
                'preferred_days': f'{offer.preferred_days}',
                'preferred_hours': f'{offer.preferred_times}',
                'preferred_classes': f'{offer.preferred_classes}',
                'preferred_teachers': ",".join([teacher.name for teacher in offer.preferred_teachers.all()]),
                'acceptable_classes': f'{offer.acceptable_classes}',
                "teacher": offer.unwanted_class.teacher.name if offer.unwanted_class.teacher else '',
                "comment": offer.additional_information if offer.additional_information else None,
            }
            items.append(item_dict)

    if request.GET.get('delete_exchange'):
        db_offers = Offer.objects.all()
        db_offers = [offer for offer in db_offers if
                     offer.exchange is not None and offer.exchange.semester == int(
                         request.GET.get('delete_exchange'))]
        for offer in db_offers:
            offer.delete()
        return redirect('/exchange/manage/{}'.format(exchange_id))

    if request.GET.get('delete_offer'):
        offer = Offer.objects.get(id=request.GET.get('delete_offer'))
        offer.delete()
        return redirect('/exchange/manage/{}'.format(exchange_id))

    return render(request, 'exchange/exchange.html', {'items': items, 'name': name, 'semester': semester})


@login_required
def manage(request):
    # Exchange.objects.all().delete()
    # for i in range(1, 11):
    #     exchange = Exchange.objects.create(
    #         name="Semester " + str(i),
    #         semester=i
    #     )
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

        return render(request, 'exchange/manage.html', {'exchanges': exchanges})
    else:
        return render(request, 'base.html')


@login_required
def offers(request):
    current_student = request.user.student
    print(Offer.STATES[0])
    db_offers = Offer.objects.filter(state=Offer.STATES[0][1]).exclude(student=current_student.id)
    # db_offers = [offer for offer in db_offers if offer.exchange.semester == current_student.semester]

    offers = [o.dictionary() for o in db_offers]
    print(offers)

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


def sign_for_class(request, unwanted_class_id, wanted_class_id):
    student = request.user.student
    unwanted = Class.objects.get(id=unwanted_class_id)
    wanted = Class.objects.get(id=wanted_class_id)

    spots_in_wanted = get_classes_free_spots(wanted)
    if spots_in_wanted > 0:
        student.list_of_classes.remove(unwanted)
        student.list_of_classes.add(wanted)
        student.save()
        return render(request, 'exchange/success.html')

    else:
        return render(request, 'exchange/failure.html')


@login_required
def add_offer(request):
    if request.method == 'POST' and 'schedule_button' in request.POST:
        print(request.POST['schedule_button'])
        unwanted_class = Class.objects.get(id=request.POST['schedule_button'])
        subject = unwanted_class.subject
        print(subject.name)

        all_classes = Class.objects.filter(subject_id=subject)
        classes_with_free_spots = []

        for clss in all_classes:
            spots = get_classes_free_spots(clss)
            if spots > 0:
                classes_with_free_spots.append(str(clss.id))

        # if sa wolne miejsca: zaznacz na inny kolor zajecia z wolnymi miejscami
        # # jesli udalo sie zapisac, wyrendereuj widok SUKCES
        # # jesli nie: przepraszamy, ktos cie ubiegl
        # # takie zajecia maja button: zapisz sie w tej chwili 

        # Tutaj dla tych wszystkich przedmiotów wyliczam dane do wyświetlenia
        all_classes = Class.objects.filter(subject_id=subject)
        all_classes = Class.objects.filter(subject=subject)
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

        return render(request, 'exchange/add_offer_new.html', {'schedule': context_schedule,
                                                               'subject_name': subject.name,
                                                               'unwanted_class_id': request.POST['schedule_button'],
                                                               'classes_with_free_spots': classes_with_free_spots})

    elif request.method == 'POST':
        print(request.POST['unwanted_class_id'])
        unwanted_class = Class.objects.get(id=request.POST['unwanted_class_id'])
        student = request.user.student

        yellow_ids, green_ids = [], []
        for color_ids, color_name in ((yellow_ids, 'yellow'), (green_ids, 'green')):
            if request.POST[color_name] != "":
                color_ids = request.POST['yellow'][:-1].split(",")

        new_offer = Offer.objects.create(
            student=request.user.student,
            # TODO
            exchange=Exchange.objects.get(semester=student.semester),
            unwanted_class=unwanted_class,
            additional_information=request.POST['comment'],
            state='New'
        )

        for green_id in green_ids:
            green_class = Class.objects.get(
                id=green_id
            )
            new_offer.preferred_classes.add(green_class)

        for yellow_id in yellow_ids:
            yellow_class = Class.objects.get(
                id=yellow_id
            )
            new_offer.acceptable_classes.add(yellow_class)

    return HttpResponseRedirect('/exchange/my-offers')


@login_required
def edit_exchange(request):
    return render(request, 'exchange/edit_exchange.html')


@login_required
def user_offers(request):
    # dynamic offers
    current_student = request.user.student
    db_offers = Offer.objects.filter(student=current_student.id).exclude(state=Offer.STATES[3])
    offers = [o.dictionary() for o in db_offers]
    # offers1=[]
    # for offer in db_offers:
    #     item_dict={
    #         "id": f'{offer.id}',
    #         "student": f'{offer.student.user.first_name} {offer.student.user.last_name}' if offer.student.user.first_name and offer.student.user.last_name else 'Anonymous',
    #         "subject": offer.unwanted_class.subject.name if offer.unwanted_class.subject.name else '',
    #         "time": f'{offer.unwanted_class.day} {offer.unwanted_`class.week} | {offer.unwanted_class.time}' if offer.unwanted_class else '',
    #         "other_times": offer.preferred_days,
    #         "teacher": offer.unwanted_class.teacher.name if offer.unwanted_class.teacher else '',
    #         "other_teachers": ",".join([teacher.name for teacher in offer.preferred_teachers.all()]),
    #         "comment": offer.additional_information if offer.additional_information else None,
    #     }
    #     offers1.append(item_dict)

    if request.GET.get('delete_user_offer'):
        offer = Offer.objects.get(id=request.GET.get('delete_user_offer'))
        offer.state = Offer.STATES[3]
        print(offer.state)
        print(Offer.STATES[3])
        offer.save()
        return redirect("/exchange/my-offers")
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
        # c = Class.objects.get(
        #             id=c_id
        #             )

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


@login_required()
def dashboard(request):
    latest_offers = Offer.objects.all().exclude(student=request.user.student)

    if len(latest_offers) > 3:
        latest_offers = latest_offers[:3]

    user_offers = Offer.objects.all().filter(student=request.user.student)

    if len(user_offers) > 3:
        user_offers = user_offers[:3]

    l_offers = [o.dictionary() for o in latest_offers]
    u_offers = [o.dictionary() for o in user_offers]

    return render(request, 'exchange/dashboard.html', {"l_offers": l_offers, "u_offers": u_offers})


@login_required()
def accept_offer(request, offer_id):
    # ta funkcja jest dosyć specyficzna bo obsługuje trzy requesty: 
    # 1. na wyświetlenie stronki "czy na pewno chcesz brać ofertę"
    # 2. na zaakceptowanie przez zainteresowanego studenta wymiany
    # 3. na ostateczne zaakceptowanie przez wystawiającego

    a_offer = Offer.objects.get(id=offer_id)

    if request.method == "POST":
        # opcja 3.
        if request.user.student == a_offer.student:
            # wyszukiwanie nowego terminu dla wystawiającego
            try:
                c_term = \
                [c for c in a_offer.other_student.list_of_classes.all() if c.subject == a_offer.unwanted_class.subject][
                    0]
            except IndexError:
                c_term = None

            # jeśli go nie znaleziono, to nic się nie dzieje
            if c_term:
                # przypisanie nowych terminóœ
                a_offer.other_student.list_of_classes.add(a_offer.unwanted_class)
                request.user.student.list_of_classes.add(c_term)

                # usunięcie starych terminów z planu godzin studentów
                request.user.student.list_of_classes.remove(a_offer.unwanted_class)
                a_offer.other_student.list_of_classes.remove(c_term)

                a_offer.state = Offer.STATES[2]

                if a_offer.other_student.subscribed:
                    send_swap_accept_mail(a_offer.other_student.user)

                request.user.student.save()
                a_offer.other_student.save()
                a_offer.save()

                messages.success(request, 'You have successfully traded your term!')

            else:
                messages.error(request, 'We could not find the other student\'s class, make sure he attends the subject.')

            return redirect('offers')

        # opcja 2.
        else:
            a_offer.other_student = request.user.student
            a_offer.state = Offer.STATES[1]
            a_offer.save()

            if a_offer.student.subscribed:
                send_offer_accept_mail(a_offer.student.user)

            messages.success(request, 'You have accepted the offer! Now wait for exchange confirmation from your fellow student.')

            return redirect('offers')

    # opcja 1.
    try:
        c_term = [c for c in request.user.student.list_of_classes.all() if c.subject == a_offer.unwanted_class.subject][
            0]
        c_term = c_term.dictionary()
    except IndexError:
        c_term = None

    return render(request, 'exchange/accept_offer.html', {"a_offer": a_offer.dictionary(), "c_term": c_term})


def decline_offer(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    offer.state = Offer.STATES[0]
    offer.save()

    return render(request, 'exchange/decline_offer.html')
