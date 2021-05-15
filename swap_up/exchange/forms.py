from django import forms
from django.forms import MultipleChoiceField, ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import *

# DAY_OF_THE_WEEK_CHOICES = [('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')]
DAY_OF_THE_WEEK_CHOICES = [('Pn', 'Pn'), ('Wt', 'Wt'), ('Śr', 'Śr'), ('Czw', 'Czw'), ('Pt', 'Pt')]
TIME_CHOICES = [('8:00', '8:00 - 9:30'), ('9:35', '9:35 - 11:05'), ('11:15', '11:15 - 12:45'),
                ('12:50', '12:50 - 14:20'), ('14:40', '14:40 - 16:10'), ('16:15', '16:15 - 17:45'), ('17:50', '17:50 - 19:20')]


class UploadFileForm(forms.Form):
    file = forms.FileField()


class AddExchangeForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True)
    semester = forms.CharField(label='Semester', max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(AddExchangeForm, self).__init__(*args, **kwargs)
        semesters = Exchange.Semester.values
        semester_choices = [(semester, semester) for semester in semesters]
        self.fields['semester'].widget = forms.Select(choices=semester_choices)




class AddOfferForm(forms.Form):
    # te pola muszą tu zostać, żeby __init__ je widział
    # to są pola korzystające z danych pobranych z bazy
    subject_name = forms.CharField(label='Subject', max_length=100, required=True)
    teacher = forms.CharField(label='Teacher', max_length=100, required=True)
    preferred_teachers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        # pobieranie aktywnego użytkownika
        self.user = kwargs.pop('user', None)

        super(AddOfferForm, self).__init__(*args, **kwargs)

        # pobieranie możliwości wyboru przedmiotu przez studenta
        classes = []
        classes = self.user.student.list_of_classes.all()

        subject_pk = []
        for c in classes:
            subject_pk.append(c.subject.pk)

        subjects = Subject.objects.filter(pk__in = subject_pk)

        # subjects = Subject.objects.filter(semester=self.user.student.semester)
        subject_choices = [(subject.subject_name, subject.subject_name) for subject in subjects]
        self.fields['subject_name'].widget = forms.Select(choices=subject_choices)

        # pobieranie dostępnych nauczycieli dla semestru poprzez znalezienie zajęć dla przedmiotów

        # for subject in subjects:
        #     classes.extend(Class.objects.filter(subject=subject))

        teachers_with_duplicates = [c.teacher.name for c in classes]
        teachers = []
        for i in teachers_with_duplicates:
            if i not in teachers:
                teachers.append(i)

        self.fields['teacher'].widget = forms.Select(choices=teachers)
        self.fields['preferred_teachers'].choices = teachers

    have_day_of_the_week = forms.CharField(
        label="Day",
        required=True,
        widget=forms.Select(choices=DAY_OF_THE_WEEK_CHOICES)
    )
    have_time = forms.CharField(
        label="Time",
        required=True,
        widget=forms.Select(choices=TIME_CHOICES)
    )
    comment = forms.CharField(label='Additional info', widget=forms.Textarea(attrs={'size': 100}))

    comment = forms.CharField(widget=forms.Textarea, required=False)

    want_time = forms.MultipleChoiceField(choices=TIME_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    want_day = forms.MultipleChoiceField(choices=DAY_OF_THE_WEEK_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)


class editOffer(forms.Form):
    def __init__(self, *args, **kwargs):
        # pobieranie aktywnego użytkownika
        self.offer = kwargs.pop('user', None)

    subject_name = forms.CharField(label='Subject', max_length=100, required=True)
    teacher = forms.CharField(label='Teacher', max_length=100, required=True)
    preferred_teachers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)

    have_day_of_the_week = forms.CharField(
        label="Day",
        required=True,
        widget=forms.Select(choices=DAY_OF_THE_WEEK_CHOICES)
    )
    have_time = forms.CharField(
        label="Time",
        required=True,
        widget=forms.Select(choices=TIME_CHOICES)
    )
    comment = forms.CharField(label='Additional info', widget=forms.Textarea(attrs={'size': 100}))

    comment = forms.CharField(widget=forms.Textarea, required=False)

    want_time = forms.MultipleChoiceField(choices=TIME_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    want_day = forms.MultipleChoiceField(choices=DAY_OF_THE_WEEK_CHOICES, widget=forms.CheckboxSelectMultiple,
                                         required=False)
