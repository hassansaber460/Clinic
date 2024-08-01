from django.contrib import admin
from .models import MedicalRap, Patient, PatientChronicDisease

# Register your models here.
admin.site.register(MedicalRap)
admin.site.register(Patient)
admin.site.register(PatientChronicDisease)
