from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Create your models here.

class Schedule(models.Model):
    DAY_CHOICES = [
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday')
    ]
    schedule_id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    work_start = models.TimeField()
    work_end = models.TimeField()

    def __str__(self):
        return f"{self.day} From {self.work_start} TO {self.work_end}"


class MedicalStaff(models.Model):
    medicalStaff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.OneToOneField('services.Profile', on_delete=models.CASCADE)
    schedule = models.ManyToManyField(Schedule, related_name='medical_schedule')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}"


class AssistantStaff(models.Model):
    MARITAL_CHOICES = [
        ('sgl', 'Single'),
        ('marr', 'Married')
    ]
    Assistant_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.OneToOneField('services.Profile', on_delete=models.CASCADE)
    schedule = models.ManyToManyField(Schedule, related_name='assistant_schedule')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    marital_status = models.CharField(max_length=4, choices=MARITAL_CHOICES)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


# الامراض المزمنة لي الطاقم الطبي
class MedicalStaffChronicDisease(models.Model):
    medical_staff_id = models.AutoField(primary_key=True)
    medical_disease = models.ForeignKey('MedicalStaff', on_delete=models.DO_NOTHING)
    chronic_disease = models.ForeignKey('medicine.TimeChronicDiseaseMedication', on_delete=models.DO_NOTHING, null=True,blank=True)

    def __str__(self):
        return (f"{self.medical_disease.user.first_name} {self.medical_disease.user.last_name}|"
                f"{self.chronic_disease.chronic_disease_medication.chronic_disease.chronic_disease_name}")


# الامراض المزمنة لي الطاقم المساعد
class AssistantStaffChronicDisease(models.Model):
    assistant_staff_id = models.AutoField(primary_key=True)
    assistant_disease = models.ForeignKey('AssistantStaff', on_delete=models.DO_NOTHING)
    chronic_disease = models.ForeignKey('medicine.TimeChronicDiseaseMedication', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return (f"{self.assistant_disease.user.firstname} {self.assistant_disease.user.lastname}|"
                f"{self.chronic_disease.chronic_disease_medication.chronic_disease.chronic_disease_name}")
