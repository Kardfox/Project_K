from django.shortcuts import redirect, render
from project.settings import BASE_DIR
from .forms import PatientForm
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

def reception(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            doctor = Doctor.objects.get(id = dict(request.POST)['doctor'][0])
            try:
                patient = Patient.objects.get(full_name = form_data['full_name'], inn = form_data['inn'], oms = form_data['oms'])
                reception = Reception.objects.create(full_name_doctor = doctor, full_name_patient = patient)
                reception.save()
                return redirect(f'{reception.id}/datetime/')
            except ObjectDoesNotExist:
                print('Patient not exist')
    else:
        form = PatientForm()
    return render(request, 'reception/reception.html', {'form' : form, 'doctors' : Doctor.objects.all(), 'style' : style('reception-style')})

def appointment_datetime(request, id):
    reception = Reception.objects.get(id = id)
    busy_time = reception.full_name_doctor.busy_time.split('\r\n')
    free_time = get_time(reception.full_name_doctor.free_time, str(reception.full_name_doctor.interval), '--')
    if request.method == 'POST':
        post_data = dict(request.POST)
        reception.datetime = datetime.combine(time_to_datetime(post_data['time'])[0], time_to_datetime(post_data['time'])[1])
        reception.save()
    return render(request, 'reception/datetime.html', {'style' : style('main-style'), 'weekdays' : list(free_time.keys()), 'free_times' : free_time})

def last_appointment(request, pk):
    last_appointment = MedicalHistory.objects.get(pk = pk)
    return render(request, 'patient/last_appointment.html', {'style' : style('main-style'), 'last_appointment' : last_appointment})