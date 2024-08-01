from django.contrib import admin
from .models import Schedule, MedicalStaff, AssistantStaff, MedicalStaffChronicDisease, AssistantStaffChronicDisease

# Register your models here.

admin.site.register(Schedule)
admin.site.register(MedicalStaff)
admin.site.register(AssistantStaff)
admin.site.register(MedicalStaffChronicDisease)
admin.site.register(AssistantStaffChronicDisease)