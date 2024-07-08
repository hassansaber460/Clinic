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
    email = models.EmailField(null=True, blank=True)
    profile = models.OneToOneField('services.Profile', on_delete=models.CASCADE)
    company = models.ForeignKey('services.Company', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
