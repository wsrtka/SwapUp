from django.db import models


class Teacher(models.Model):
    __first_name = models.CharField(max_length=30)
    __last_name = models.CharField(max_length=30)
    __title = models.CharField(max_length=30)

    def __init__(self, first_name, last_name, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__first_name = first_name
        self.__last_name = last_name
        self.__title = title

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
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title
