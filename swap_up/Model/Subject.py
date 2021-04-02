from django.db import models


class Subject:
    __subject_name = models.CharField(max_length=30)
    __type = models.CharField(max_length=30)
    __semester = models.IntegerField()
    __path = models.CharField(max_length=30)
    __mandatory = models.BooleanField()

    def __init__(self, subject_name, type, semester, path, mandatory):
        self.__subject_name = subject_name
        self.__type = type
        self.__semester = semester
        self.__path = path
        self.__mandatory = mandatory

    @property
    def subject_name(self):
        return self.__subject_name

    @subject_name.setter
    def subject_name(self, name):
        self.__subject_name = name

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def semester(self):
        return self.__semester

    @semester.setter
    def semester(self, semester):
        self.__semester = semester

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def mandatory(self):
        return self.__mandatory

    @mandatory.setter
    def mandatory(self, mandatory):
        self.__mandatory = mandatory
