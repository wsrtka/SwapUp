from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


PATHS = [
        ('A', 'Algorythmic path'),
        ('AA', 'Algorythmic-application path'),
        ('SD', 'Software development path')
    ]

class Semester(models.IntegerChoices):
        SEM1 = 1
        SEM2 = 2
        SEM3 = 3
        SEM4 = 4
        SEM5 = 5
        SEM6 = 6
        SEM7 = 7
        SEM8 = 8
        SEM9 = 9
        SEM10 = 10

class Exchange(models.Model):
    
    creation_time = models.DateTimeField(auto_now_add=True, null=True)
    modification_time = models.DateTimeField(auto_now=True, null=True)
    end_time = models.DateTimeField(null=True)
    name = models.CharField(max_length=30, null=True)
    semester = models.IntegerField(choices=Semester.choices, null=True)

    def __str__(self):
        return f'Exchange of semester {self.semester}'


class Subject(models.Model):

    name = models.CharField(max_length=30, null=True)
    category = models.CharField(max_length=30, null=True)
    path = models.CharField(max_length=30, choices=PATHS, null=True)
    semester = models.IntegerField(choices=Semester.choices, null=True)
    mandatory = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.subject_name}, s{self.semester}, {self.path}'


class Teacher(models.Model):

    TITLES = [
        ('inż.', 'inżynier'),
        ('mgr. inż.', 'magister inżynier'),
        ('dr.', 'doktor'),
        ('dr. inż.', 'doktor inżynier')
    ]

    name = models.CharField(max_length=60, null=True)
    title = models.CharField(max_length=30, choices=TITLES, null=True)

    def __str__(self):
        return f'{self.title} {self.name}'


class Class(models.Model):

    WEEK_CHOICES = [
        ('A', 'Week A'),
        ('B', 'Week B')
    ]

    DAY_CHOICES = [
        ('Pn', 'Poniedziałek'),
        ('Wt', 'Wtorek'),
        ('Śr', 'Środa'),
        ('Czw', 'Czwartek'),
        ('Pt', 'Piątek')
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES, null=True)
    time = models.TimeField(null=True)
    capacity = models.IntegerField(null=True)
    week = models.CharField(max_length=1, choices=WEEK_CHOICES, null=True)

    group_number = models.IntegerField(null=True)
    room = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.subject}, {self.teacher}, {self.time} {self.day}, {self.room}'

    def dictionary(self):
        class_dict = {}

        class_dict['subject'] = self.subject.name
        class_dict['teacher'] = self.teacher.name
        class_dict['day'] = self.day
        class_dict['time'] = self.time
        class_dict['week'] = self.week

        return class_dict


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    index_number = models.IntegerField(unique=True, null=True)
    semester = models.IntegerField(null=True)
    path = models.CharField(max_length=40, choices=PATHS, null=True)

    list_of_additional_subjects = models.ManyToManyField(Subject)  
    list_of_classes = models.ManyToManyField(Class)  

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}, {self.index_number}, s{self.semester}'


class Offer(models.Model):

    STATES = [
        ('N', 'New'),
        ('P', 'Pending'),
        ('C', 'Closed')
    ]

    # meta info
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=10, choices=STATES, default=STATES[0])
    add_time = models.DateTimeField(auto_now_add=True, null=True)

    # offer info
    unwanted_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='unwanted_class', null=True)
    preferred_days = None
    preferred_times = None
    preferred_classes = models.ManyToManyField(Class, related_name='user_green')
    acceptable_classes = models.ManyToManyField(Class, related_name='user_yellow')
    preferred_teachers = models.ManyToManyField(Teacher)
    additional_information = models.CharField(max_length=100, null=True)

    # "transaction" info
    other_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='wantee')
    other_offer = models.ForeignKey("Offer", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.state} offer from {self.student.user.username}'

    def dictionary(self):
        offer_dict = {}

        offer_dict['student'] = f'{self.student.user.first_name} {self.student.user.last_name}' if self.student.user.first_name and self.student.user.last_name else 'Anonymous'
        offer_dict['subject'] = self.unwanted_class.subject.name if self.unwanted_class.subject.name else ''
        offer_dict['time'] = f'{self.unwanted_class.day} {self.unwanted_class.week}, {self.unwanted_class.time}' if self.unwanted_class else ''
        offer_dict['teacher'] = self.unwanted_class.teacher.name if self.unwanted_class.teacher else ''
        offer_dict['comment'] = self.additional_information if self.additional_information else None
        offer_dict['preferred_days'] = self.preferred_days
        offer_dict['preferred_hours'] = self.preferred_times
        offer_dict['preferred_teachers'] = [teacher.name for teacher in self.preferred_teachers.all()]
        offer_dict['id'] = self.id
        offer_dict['date'] = self.add_time

        return offer_dict