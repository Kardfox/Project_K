from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('full_name', 'inn', 'oms', 'home_adress', 'email', 'telephone')

