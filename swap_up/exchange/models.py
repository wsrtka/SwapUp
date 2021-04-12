from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Exchange(models.Model):
    creation_date = models.DateField()
    modification_date = models.DateField()
    name = models.CharField(max_length=30)
    semester = models.IntegerField()

    @property
    def creation_date(self):
        return self.creation_date

    @creation_date.setter
    def creation_date(self,date):
        self.creation_date=date

    @property
    def modification_date(self):
        return  self.modification_date

    @modification_date.setter
    def modification_date(self, date):
        self.modification_date=date

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self,name):
        self.name=name

    @property
    def semester(self):
        return self.semester

    @semester.setter
    def semester(self, semester):
        self.semester=semester



class Subject(models.Model):
    subject_name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    semester = models.IntegerField()
    path = models.CharField(max_length=30)
    mandatory = models.BooleanField()

    @property
    def subject_name(self):
        return self.subject_name

    @subject_name.setter
    def subject_name(self, name):
        self.subject_name = name

    @property
    def category(self):
        return self.category

    @category.setter
    def category(self, type):
        self.category = type

    @property
    def semester(self):
        return self.semester

    @semester.setter
    def semester(self, semester):
        self.semester = semester

    @property
    def path(self):
        return self.path

    @path.setter
    def path(self, path):
        self.path = path

    @property
    def mandatory(self):
        return self.mandatory

    @mandatory.setter
    def mandatory(self, mandatory):
        self.mandatory = mandatory


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    title = models.CharField(max_length=30, null=True)

    @property
    def first_name(self):
        return self.first_name

    @first_name.setter
    def first_name(self, name):
        self.first_name = name

    @property
    def last_name(self):
        return self.last_name

    @last_name.setter
    def last_name(self, name):
        self.last_name = name

    @property
    def title(self):
        return self.title

    @title.setter
    def title(self, title):
        self.title = title


class Class(models.Model):

    WEEK_CHOICES = [
        ('A', 'Week A'),
        ('B', 'Week B')
    ]
    
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    day = models.DateField()
    time = models.TimeField()
    capacity = models.IntegerField()
    week = models.CharField(max_length=1, choices=WEEK_CHOICES)


class Student(models.Model):
    index_number = models.IntegerField(unique=True, null=True)
    semester = models.IntegerField(null=True)

    # list_of_additional_subjects = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)    # tutaj nie jestem pewien czy normalne settery
    # list_of_classes = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)                  # będą działały więc póki co zostawiam bez

    list_of_additional_subjects = models.ManyToManyField(Subject, blank=True)  # tutaj nie jestem pewien czy normalne settery
    list_of_classes = models.ManyToManyField(Class, blank=True)  # będą działały więc póki co zostawiam bez

    path = models.CharField(max_length=40, null=True)
    # tutaj łączymy studenta z użytkownikiem
    # User w Django ma imie, nazwisko, email
    # ma też grupy, i te grupy będą związane z określonymi uprawnieniami
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def index_number(self):
        return self.index_number

    @index_number.setter
    def index_number(self, number):
        self.index_number = number

    @property
    def semester(self):
        return self.semester

    @semester.setter
    def semester(self, semester):
        self.semester = semester

    @property
    def path(self):
        return self.path

    @path.setter
    def path(self, path):
        self.path = path


class Offer(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    preferred_class_id_list = None
    additional_information = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    other_student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    other_offer_id = models.IntegerField()
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, default=None)

    @property
    def additional_information(self):
        return self.additional_information

    @additional_information.setter
    def additional_information(self, additional_information):
        self.additional_information = additional_information

    @property
    def state(self):
        return self.state

    @state.setter
    def state(self, state):
        self.state = state

    @property
    def other_student_id(self):
        return self.other_student_id

    @other_student_id.setter
    def other_student_id(self, other_student_id):
        self.other_student_id = other_student_id

    @property
    def other_exchange_id(self):
        return self.other_exchange_id

    @other_exchange_id.setter
    def other_exchange_id(self, other_exchange_id):
        self.other_exchange_id = other_exchange_id

    @property
    def preferred_class_id_list(self):
        return self.preferred_class_id_list

    @preferred_class_id_list.setter
    def preferred_class_id_list(self, preferred_class_id_list):
        self.preferred_class_id_list = preferred_class_id_list

    @property
    def class_id(self):
        return self.class_id

    @class_id.setter
    def class_id(self, class_id):
        self.class_id = class_id
