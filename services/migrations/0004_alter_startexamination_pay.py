# Generated by Django 5.0.6 on 2024-07-08 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_profile_city_alter_profile_government_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startexamination',
            name='pay',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
