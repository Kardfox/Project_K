# Generated by Django 3.1.2 on 2020-11-15 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201113_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firstreception',
            name='datetime',
        ),
        migrations.RemoveField(
            model_name='firstreception',
            name='full_name_doctor',
        ),
        migrations.RemoveField(
            model_name='firstreception',
            name='full_name_patient',
        ),
    ]
