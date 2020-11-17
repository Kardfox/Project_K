from django.shortcuts import redirect, render
from project.settings import BASE_DIR
from .models import*
from .desired_functions import*
from django.core.exceptions import ObjectDoesNotExist


def main(request):
    return render(request, 'app/main.html', {'style' : style('main-style'), 'doctors' : Doctor.objects.all()})

def personal_cabinet(request):
    validation = ''
    if request.method == 'POST':
        post_data = dict(request.POST)
        try:
            patient = Patient.objects.get(full_name = post_data['full_name'][0])
            if post_data['oms'][0] == patient.oms:
                future_appointments = revealing_olds_objs(Reception.objects.filter(full_name_patient = patient.pk))
                last_appointments = MedicalHistory.objects.filter(full_name_patient = patient.pk)
                med_price_link_name = []
                for med in patient.appointment_med.split('\n'):
                    med_price_link_name.append([med, f'https://apteka.ru/search/?q={med}', get_price(med)])
                return render(request, 'patient/card.html', {'style' : style('main-style'), 'meds' : med_price_link_name, 'future_appointments' : future_appointments, 'patient' : patient, 'last_appointments' : last_appointments, 'len_future_appointments' : len(future_appointments)})
            else:
                validation = 'Неверный ОМС'
        except ObjectDoesNotExist:
            validation = 'Неверное ФИО'
    return render(request, 'patient/login.html', {'style' : style('login-style'), 'validation' : validation})

def reception_patient(request):
    if request.method == 'POST':
        post_data = dict(request.POST)
        try:
            patient = Patient.objects.get(full_name = post_data['full_name'][0], inn = post_data['inn'][0], oms = post_data['oms'][0])
        except ObjectDoesNotExist:
            patient = Patient.objects.create(full_name = post_data['full_name'], inn = post_data['inn'], oms = post_data['oms'], home_adress = post_data['home_adress'], email = post_data['email'], telephone = post_data['telephone'])
            patient.save()
        return redirect(f'{patient.pk}/doctor/')
    return render(request, 'reception/patient.html', {'style' : style('reception-patient-style')})

def reception_doctor(request, patient_pk):
    patient = Patient.objects.get(pk = patient_pk)
    if request.method == 'POST':
        post_data = dict(request.POST)
        doctor = Doctor.objects.get(full_name = post_data['doctor'][0])
        new_reception = Reception.objects.create(full_name_doctor = doctor, full_name_patient = patient)
        new_reception.save()
        return redirect(f'/reception/{new_reception.pk}/datetime/')
    return render(request, 'reception/doctor.html', {'style' : style('main-style'), 'doctors' : Doctor.objects.all()})

def reception_datetime(request, pk):
    reception = Reception.objects.get(pk = pk)
    busy_time = str_list_to_time_list(reception.full_name_doctor.busy_time.split('\r\n'))
    schedule = get_time(reception.full_name_doctor.free_time, str(reception.full_name_doctor.interval))
    free_time = []
    for time in schedule:
        if time in busy_time:
            continue
        else:
            free_time.append(time)
    if request.method == 'POST':
        post_data = dict(request.POST)
        reception_datetime = time_to_datetime(post_data['time'])
        reception.datetime = datetime.combine(reception_datetime[0], reception_datetime[1])
        reception.save()
        return redirect(f'/reception/{reception.pk}/info/')
    return render(request, 'reception/datetime.html', {'style' : style('main-style'), 'weekdays' : WEEKDAYS, 'free_times' : free_time})

def reception_info(request, pk):
    reception = Reception.objects.get(pk = pk)
    return render(request, 'reception/info.html', {'reception' : reception})

def last_appointment(request, pk):
    last_appointment = MedicalHistory.objects.get(pk = pk)
    return render(request, 'patient/last_appointment.html', {'style' : style('main-style'), 'last_appointment' : last_appointment})