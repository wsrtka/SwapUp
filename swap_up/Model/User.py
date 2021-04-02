from django.db import models
import swap_up.Model.Subject as Subject
import swap_up.Model.Class as Class

class User(models.Model):
    __first_name = models.CharField(max_length=30)
    __last_name = models.CharField(max_length=30)
    __index_number = models.IntegerField()
    __year = models.IntegerField()
    __role = models.CharField(max_length=10)
    __mail = models.CharField(max_length=40)
    __list_of_additional_subjects = models.ForeignKey(Subject,
                                                      on_delete=models.CASCADE)  # tutaj nie jestem pewien czy normalne settery
    __list_of_classes = models.ForeignKey(Class, on_delete=models.CASCADE)  # będą działały więc póki co zostawiam bez
    __path = models.CharField(max_length=40)

    def __init__(self, first_name, last_name, index_number, year, role, mail, path):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__year = year
        self.__index_number = index_number
        self.__role = role
        self.__mail = mail
        self.__path = path

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, name):
        self.__first_name = name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, name):
        self.__last_name = name

    @property
    def index_number(self):
        return self.__index_number

    @index_number.setter
    def index_number(self, number):
        self.__index_number = number

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year):
        self.__year = year

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role

    @property
    def mail(self):
        return self.__mail

    @mail.setter
    def mail(self, mail):
        self.__mail = mail

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path
