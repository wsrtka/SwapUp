from django import forms
from django.forms import MultipleChoiceField, ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import *


DAY_OF_THE_WEEK_CHOICES = [('MON', 'Monday'), ('TUE','Tuesday'), ('WED','Wednesday'), ('THU','Thursday'), ('FRI','Friday')]
TIME_CHOICES = [('8-00', '8:30 - 9:30'), ('9-35', '9:35 - 11:05'), ('11-15', '11:15 - 12:45'),
 ('12-50', '12:50 - 14:20'), ('14-40', '14:40 - 16:10'), ('16-15', '16:15 - 17:45'), ('17-50', '17:50 - 19:20')]


class UploadFileForm(forms.Form):
    file = forms.FileField()


class AddOfferForm(forms.Form):
    
    subject_name = forms.CharField(label='Subject', max_length=100, required=True)
    teacher = forms.CharField(label='Teacher', max_length=100, required=True)
    preferred_teachers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)
    
        super(AddOfferForm, self).__init__(*args, **kwargs)

        subjects = Subject.objects.filter(semester=self.user.student.semester)
        subject_choices = [(subject.subject_name[0], subject.subject_name) for subject in subjects]
        self.fields['subject_name'].widget = forms.Select(choices=subject_choices)

        classes = []

        for subject in subjects:
            classes.extend(Class.objects.filter(subject_id=subject))

        teachers = [(c.teacher_id.last_name[0], c.teacher_id.last_name) for c in classes]
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
    comment = forms.CharField(label='Additional info', widget=forms.Textarea(attrs={'size':100}))

    comment = forms.CharField(widget=forms.Textarea, required=False)    

    want_time = forms.MultipleChoiceField(choices = TIME_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    want_day = forms.MultipleChoiceField(choices = DAY_OF_THE_WEEK_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)