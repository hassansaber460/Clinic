from django.contrib import admin
from .models import (StartExamination, TypeExamination, Company, Profile, Examination, MedicalRapContent,
                     TransferLetters, MedicalReports)

# Register your models here.
admin.site.register(Profile)
admin.site.register(StartExamination)
admin.site.register(Examination)
admin.site.register(TypeExamination)
admin.site.register(Company)
admin.site.register(MedicalRapContent)
admin.site.register(TransferLetters)
admin.site.register(MedicalReports)
