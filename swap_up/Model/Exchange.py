from django.db import models
import swap_up.Model.Class as Class
import swap_up.Model.User as User


class Exchange:
    __student_id = None  # tutaj nie jestem pewien co to ma być?
    # to ma być FK do klasy User czy sobie generujemy nowy id dla studenta?
    __class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    __preferred_class_id_list = None  # to chyba nie będzie miało odzwierciedlenia w bazie
    # bo w bazie w jednej komórce nie można trzymać list więc chyba lepiej to zostawić jako lista pythonowska
    __additional_information = models.CharField(max_length=100)
    __state = models.CharField(max_length=10)
    __other_student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    __other_exchange_id = models.IntegerField()

    def __init__(self, info, state, other_student_id, other_exchange_id):
        self.__additional_information = info
        self.__state = state
        self.__other_exchange_id = other_exchange_id
        self.__other_student_id = other_student_id

    @property
    def additional_information(self):
        return self.__additional_information

    @additional_information.setter
    def additional_information(self, additional_information):
        self.__additional_information = additional_information

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def other_student_id(self):
        return self.__other_student_id

    @other_student_id.setter
    def other_student_id(self, other_student_id):
        self.__other_student_id = other_student_id

    @property
    def other_exchange_id(self):
        return self.__other_exchange_id

    @other_exchange_id.setter
    def other_exchange_id(self, other_exchange_id):
        self.__other_exchange_id = other_exchange_id

    @property
    def preferred_class_id_list(self):
        return self.__preferred_class_id_list

    @preferred_class_id_list.setter
    def preferred_class_id_list(self,preferred_class_id_list):
        self.__preferred_class_id_list=preferred_class_id_list

    @property
    def class_id(self):
        return self.__class_id

    @class_id.setter
    def class_id(self, class_id):
        self.__class_id=class_id