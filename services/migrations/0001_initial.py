# Generated by Django 5.0.6 on 2024-07-08 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=50)),
                ('company_email', models.EmailField(max_length=254, null=True)),
                ('phone', models.CharField(max_length=11)),
                ('discount_percentage', models.IntegerField()),
                ('start_contract', models.DateField()),
                ('end_contract', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('examination_id', models.AutoField(primary_key=True, serialize=False)),
                ('height', models.PositiveIntegerField(blank=True, null=True)),
                ('temperature', models.PositiveIntegerField(blank=True, null=True)),
                ('weight', models.PositiveIntegerField(blank=True, null=True)),
                ('pulse', models.PositiveIntegerField(blank=True, null=True)),
                ('pressure', models.CharField(blank=True, max_length=150, null=True)),
                ('head_circumference', models.PositiveIntegerField(blank=True, null=True)),
                ('medical_diagnosis', models.TextField(blank=True, null=True)),
                ('medicine', models.CharField(blank=True, max_length=200, null=True)),
                ('analysis', models.CharField(blank=True, max_length=100, null=True)),
                ('reexamination_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('blood_type', models.CharField(choices=[('A+', 'A positive'), ('A-', 'A negative'), ('B+', 'B positive'), ('B-', 'B negative'), ('AB+', 'AB positive'), ('AB-', 'AB negative'), ('O+', 'O positive'), ('O-', 'O negative')], max_length=3)),
                ('date_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('Government', models.CharField(max_length=50, null=True)),
                ('City', models.CharField(max_length=50, null=True)),
                ('photo', models.ImageField(blank=True, upload_to='services/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='StartExamination',
            fields=[
                ('startExamination_id', models.AutoField(primary_key=True, serialize=False)),
                ('pay', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='TypeExamination',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_examination', models.CharField(max_length=100)),
                ('discount_for_type_examination', models.BooleanField()),
                ('price_examination', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNoProfile',
            fields=[
                ('phoneNo_id', models.AutoField(primary_key=True, serialize=False)),
                ('phoneNo', models.CharField(max_length=11, unique=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.profile')),
            ],
        ),
    ]
