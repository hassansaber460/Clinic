from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    BLOOD_CHOICES = [
        ('A+', 'A positive'),
        ('A-', 'A negative'),
        ('B+', 'B positive'),
        ('B-', 'B negative'),
        ('AB+', 'AB positive'),
        ('AB-', 'AB negative'),
        ('O+', 'O positive'),
        ('O-', 'O negative')
    ]
    profile_id = models.AutoField(primary_key=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_CHOICES, blank=True, null=True)
    date_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Government = models.CharField(max_length=50, null=True, blank=True)
    City = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='services/%Y/%m/%d', blank=True)


class PhoneNoProfile(models.Model):
    phoneNo_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    phoneNo = models.CharField(max_length=11, unique=True)


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50)
    company_email = models.EmailField(null=True)
    phone = models.CharField(max_length=11)
    discount_percentage = models.IntegerField()
    start_contract = models.DateField()
    end_contract = models.DateField()

    def __str__(self):
        return self.company_name


# Settings
class TypeExamination(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_examination = models.CharField(max_length=100)
    discount_for_type_examination = models.BooleanField(default=False)
    price_examination = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type_examination}"


class StartExamination(models.Model):
    startExamination_id = models.AutoField(primary_key=True)
    queue = models.OneToOneField('communication.Queue', on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey('visitors.Patient', on_delete=models.CASCADE)
    medical = models.ForeignKey('staff.MedicalStaff', on_delete=models.CASCADE)
    assistant = models.ForeignKey('staff.AssistantStaff', on_delete=models.CASCADE)
    type_examination = models.ForeignKey('TypeExamination', on_delete=models.CASCADE, null=True)
    pay = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)

    def __str__(self):
        return f"{self.patient.firstName} {self.patient.lastName}"


class Examination(models.Model):
    examination_id = models.AutoField(primary_key=True)
    start_examination = models.OneToOneField('StartExamination', on_delete=models.CASCADE)
    height = models.PositiveIntegerField(null=True, blank=True)
    temperature = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    pulse = models.PositiveIntegerField(null=True, blank=True)
    pressure = models.CharField(max_length=150, null=True, blank=True)
    head_circumference = models.PositiveIntegerField(null=True, blank=True)
    medical_diagnosis = models.TextField(null=True, blank=True)
    medicine = models.CharField(max_length=200, null=True, blank=True)
    analysis = models.CharField(max_length=100, null=True, blank=True)
    reexamination_date = models.DateField()

    def __str__(self):
        return f"{self.start_examination.patient.firstName} {self.start_examination.patient.lastName}"


# save payment Examination using database
@receiver(post_save, sender=StartExamination)
def save_pay(sender, instance, created, **kwargs):
    if created:
        if instance.type_examination.discount_for_type_examination:
            discount_percentage = Decimal(instance.patient.company.discount_percentage)
            instance.pay = (instance.type_examination.price_examination
                            - (instance.type_examination.price_examination * (discount_percentage / Decimal(100))))
        else:
            instance.pay = instance.type_examination.price_examination
        instance.save()
    else:
        if instance.type_examination.discount_for_type_examination:
            discount_percentage = Decimal(instance.patient.company.discount_percentage)
            pay = (instance.type_examination.price_examination
                   - (instance.type_examination.price_examination * (discount_percentage / Decimal(100))))
            StartExamination.objects.filter(startExamination_id=instance.startExamination_id).update(pay=pay)
        else:
            pay = instance.type_examination.price_examination
            StartExamination.objects.filter(startExamination_id=instance.startExamination_id).update(pay=pay)
