# Generated by Django 5.0.6 on 2024-07-08 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='City',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Government',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='blood_type',
            field=models.CharField(blank=True, choices=[('A+', 'A positive'), ('A-', 'A negative'), ('B+', 'B positive'), ('B-', 'B negative'), ('AB+', 'AB positive'), ('AB-', 'AB negative'), ('O+', 'O positive'), ('O-', 'O negative')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='typeexamination',
            name='discount_for_type_examination',
            field=models.BooleanField(default=False),
        ),
    ]