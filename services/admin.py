from django.contrib import admin
from .models import StartExamination, TypeExamination, Company, Profile, PhoneNoProfile, Examination

# Register your models here.
admin.site.register(Profile)
admin.site.register(PhoneNoProfile)
admin.site.register(StartExamination)
admin.site.register(Examination)
admin.site.register(TypeExamination)
admin.site.register(Company)


