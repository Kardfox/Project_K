from django.db import models
from django.contrib.auth.models import User



class Patient(models.Model):
    full_name = models.CharField(max_length = 40, verbose_name = 'ФИО')
    inn = models.CharField(max_length = 10, verbose_name = 'ИНН')
    oms = models.CharField(max_length = 16, verbose_name = 'Номер ОМС')
    home_adress = models.CharField(max_length = 100, verbose_name = 'Домашний адрес')
    email = models.EmailField(verbose_name = 'Электронная почта')
    telephone = models.CharField(max_length = 16, verbose_name = 'Номер телефона')
    appointment = models.TextField(null = True, blank = True)
    appointment_med = models.TextField(verbose_name = 'Лекарства', null = True, blank = True)

    def __str__(self):
        return self.full_name

class Doctor(models.Model):
    full_name = models.CharField(max_length = 40, verbose_name = 'ФИО')
    position = models.CharField(max_length = 15, verbose_name = 'Должность')
    plots = models.CharField(max_length = 100, verbose_name = 'Участки')
    cabinet = models.PositiveIntegerField(verbose_name = 'Кабинет')
    telephone = models.CharField(max_length = 16, verbose_name = 'Номер телефона')
    free_time = models.TextField(verbose_name = 'График работы')
    interval = models.TimeField(verbose_name = 'Длина приема', default = '1:00:00')
    busy_time = models.TextField(verbose_name = 'Занятое время', null = True, blank = True)

    def __str__(self):
        return self.full_name + ', ' + self.position

'''class FirstReception(models.Model):
    full_name_doctor = models.ForeignKey(Doctor, on_delete = models.DO_NOTHING, verbose_name = 'ФИО доктора')
    full_name_patient = models.ForeignKey(Patient, on_delete = models.DO_NOTHING, verbose_name = 'ФИО пациента')
    appointment = models.TextField(verbose_name = 'Назначения', null = True, blank = True)
    appointment_med = models.TextField(verbose_name = 'Лекарства', null = True, blank = True)
    datetime = models.DateTimeField(verbose_name = 'Дата и время приема', null = True, blank = True)

class SecondReception(models.Model):
    full_name_doctor = models.ForeignKey(Doctor, on_delete = models.DO_NOTHING, verbose_name = 'ФИО доктора')
    full_name_patient = models.ForeignKey(Patient, on_delete = models.DO_NOTHING, verbose_name = 'ФИО пациента')
    appointment = models.TextField(verbose_name = 'Назначения')
    appointment_med = models.TextField(verbose_name = 'Лекарства')
    datetime = models.DateTimeField(verbose_name = 'Дата и время приема', null = True)'''

class Reception(models.Model):
    full_name_doctor = models.ForeignKey(Doctor, on_delete = models.DO_NOTHING, verbose_name = 'ФИО доктора')
    full_name_patient = models.ForeignKey(Patient, on_delete = models.DO_NOTHING, verbose_name = 'ФИО пациента')
    datetime = models.DateTimeField(verbose_name = 'Дата и время приема', null = True)

    def __str__(self):
        return f'{self.full_name_doctor.full_name}, {self.full_name_doctor.position}({self.datetime})'

class MedicalHistory(models.Model):
    full_name_patient = models.ForeignKey(Patient, on_delete = models.DO_NOTHING, verbose_name = 'ФИО пациента')
    service = models.CharField(max_length = 30, verbose_name = 'Услуга')
    сomplaints = models.TextField(verbose_name = 'Жалобы при обращении')
    anamnesis = models.CharField(max_length = 30, verbose_name = 'Анамнез')
    objective_status = models.CharField(max_length = 30, verbose_name = 'Объективный статус')
    appointment = models.TextField(verbose_name = 'Назначения')
    appointment_med = models.TextField(verbose_name = 'Лекарства')
    addiction_diseases = models.TextField(verbose_name = 'Сопутствующие заболевания')
    doctor = models.ForeignKey(Doctor, on_delete = models.DO_NOTHING, verbose_name = 'Доктор')
    datetime = models.DateTimeField(verbose_name = 'Дата и время')

    def __str__(self):
        return f'{str(self.datetime.date())}({str(self.datetime.time())}) - {self.doctor.full_name}, {self.doctor.position}'