from django.db import models
import swap_up.Model.Subject as Subject
import swap_up.Model.Teacher as Teacher


class Class:
    __subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    __day = models.DateField()
    __time = models.TimeField()
    __row = models.CharField(max_length=20)
    __teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __init__(self, day, time, row):
        self.__day = day
        self.__row = row
        self.__time = time

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        self.__day = day

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, row):
        self.__row = row

    @property
    def subject_id(self):
        return self.__subject_id

    @subject_id.setter
    def subject_id(self, subject_id):
        self.__subject_id = subject_id
