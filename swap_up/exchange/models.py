from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

PATHS = [
    ('A', 'Algorythmic path'),
    ('AA', 'Algorythmic-application path'),
    ('SD', 'Software development path')
]


class Exchange(models.Model):
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

    def __str__(self):
        return self.name

    creation_date = models.DateField(null=True)
    modification_date = models.DateField(null=True)
    name = models.CharField(max_length=30, null=True)
    semester = models.IntegerField(choices=Semester.choices, null=True)


class Subject(models.Model):
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

    # def __str__(self):
    #     return self.subject_name

    subject_name = models.CharField(max_length=30, null=True)
    category = models.CharField(max_length=30, null=True)
    path = models.CharField(max_length=30, choices=PATHS, null=True)
    semester = models.IntegerField(choices=Semester.choices, null=True)
    mandatory = models.BooleanField(null=True)


class Teacher(models.Model):
    TITLES = [
        ('inż.', 'inżynier'),
        ('mgr. inż.', 'magister inżynier'),
        ('dr.', 'doktor'),
        ('dr. inż.', 'doktor inżynier')
    ]

    def __str__(self):
        return self.last_name

    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    title = models.CharField(max_length=30, choices=TITLES, null=True)


class Class(models.Model):
    WEEK_CHOICES = [
        ('A', 'Week A'),
        ('B', 'Week B')
    ]

    def __str__(self):
        return self.day

    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

    day = models.CharField(max_length=10, null=True)
    time = models.TimeField(null=True)
    capacity = models.IntegerField(null=True)
    week = models.CharField(max_length=1, choices=WEEK_CHOICES, null=True)

    group_number = models.IntegerField(null=True)
    room = models.CharField(max_length=20, null=True)


class Student(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    index_number = models.IntegerField(unique=True, null=True)
    semester = models.IntegerField(null=True)
    path = models.CharField(max_length=40, choices=PATHS, null=True)

    # list_of_additional_subjects = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)    # tutaj nie jestem pewien czy normalne settery
    # list_of_classes = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)                  # będą działały więc póki co zostawiam bez

    list_of_additional_subjects = models.ManyToManyField(Subject)  # tutaj nie jestem pewien czy normalne settery
    list_of_classes = models.ManyToManyField(Class)  # będą działały więc póki co zostawiam bez


class Offer(models.Model):
    STATES = [
        ('N', 'New'),
        ('P', 'Pending'),
        ('C', 'Closed')
    ]

    def __str__(self):
        return self.additional_information

    # meta info
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=10, choices=STATES, default=STATES[0])

    # offer info
    unwanted_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='unwanted_class', null=True)
    preferred_days = None
    preferred_times = None
    # to będzie kiedyś, na to teraz sobie nie możemy pozwolić xd
    # preferred_classes = models.ManyToManyField(Class, related_name='user_preferences')
    preferred_teachers = models.ManyToManyField(Teacher)
    additional_information = models.CharField(max_length=100, null=True)

    # "transaction" info
    other_student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    other_offer = models.IntegerField(null=True)
