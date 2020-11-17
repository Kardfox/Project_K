from django.contrib import admin
from .models import*

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(MedicalHistory)
admin.site.register(Reception)
#admin.site.register(FirstReception)
#admin.site.register(SecondReception)