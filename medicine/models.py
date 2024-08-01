from django.db import models


# Create your models here.

# اسماء الامراض المزمنه
class ChronicDisease(models.Model):
    chronic_disease_id = models.AutoField(primary_key=True)
    chronic_disease_name = models.CharField(max_length=100)

    def __str__(self):
        return self.chronic_disease_name


# العلاج لي الامراض المزمنة
class Treatment(models.Model):
    treatment_id = models.AutoField(primary_key=True)
    treatment_name = models.CharField(max_length=100)

    def __str__(self):
        return self.treatment_name


# مواعيد التناول الادوية الخاصة بالامراض المزمنه
class TimeTakeTreatment(models.Model):
    time_take_id = models.AutoField(primary_key=True)
    take_treatment = models.CharField(max_length=100)

    def __str__(self):
        return self.take_treatment


# ربط المرض المزمن بالدواء الخاص بة
class ChronicDiseaseMedication(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    chronic_disease = models.ForeignKey('ChronicDisease', on_delete=models.CASCADE)
    treatment = models.ForeignKey('Treatment', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.chronic_disease.chronic_disease_name} {self.treatment.treatment_name}"


# مواعيد التناول الادوية الخاصة بالامراض المزمنه
class TimeChronicDiseaseMedication(models.Model):
    time_id = models.AutoField(primary_key=True)
    chronic_disease_medication = models.ForeignKey('ChronicDiseaseMedication', on_delete=models.CASCADE)
    time_take_treatment = models.ForeignKey('TimeTakeTreatment', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.time_take_treatment.take_treatment}"


class MedicineUseInClinic(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=150)

    def __str__(self):
        return self.medicine_name


class TakeMedicine(models.Model):
    Take_id = models.AutoField(primary_key=True)
    Method_taken = models.CharField(max_length=200)

    def __str__(self):
        return self.Method_taken


class MedicationReference(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.ForeignKey('MedicineUseInClinic', on_delete=models.CASCADE)
    Method_taken = models.ManyToManyField('TakeMedicine', related_name='reference')

    def __str__(self):
        return self.medicine_name.medicine_name
