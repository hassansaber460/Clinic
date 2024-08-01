from django.db import models


# Create your models here.

class MedicalRap(models.Model):
    medicalRap_id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    profile = models.OneToOneField('services.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    ssn = models.CharField(max_length=14, unique=True, null=True)
    email = models.EmailField(null=True, blank=True)
    profile = models.OneToOneField('services.Profile', on_delete=models.CASCADE)
    company = models.ForeignKey('services.Company', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


# الادوية المزمنه لي المرضي
class PatientChronicDisease(models.Model):
    patient_chronic_disease_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patient', on_delete=models.DO_NOTHING)
    chronic_disease = models.ForeignKey('medicine.TimeChronicDiseaseMedication', on_delete=models.DO_NOTHING)

    def __str__(self):
        return (f"{self.patient.firstName} {self.patient.lastName}|"
                f"{self.chronic_disease.chronic_disease_medication.chronic_disease.chronic_disease_name}")
