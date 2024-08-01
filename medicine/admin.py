from django.contrib import admin
from .models import ChronicDisease, ChronicDiseaseMedication, TimeChronicDiseaseMedication, TimeTakeTreatment, Treatment, MedicineUseInClinic, TakeMedicine

# Register your models here.

admin.site.register(ChronicDisease)
admin.site.register(ChronicDiseaseMedication)
admin.site.register(TimeTakeTreatment)
admin.site.register(Treatment)
admin.site.register(TimeChronicDiseaseMedication)
admin.site.register(MedicineUseInClinic)
admin.site.register(TakeMedicine)

