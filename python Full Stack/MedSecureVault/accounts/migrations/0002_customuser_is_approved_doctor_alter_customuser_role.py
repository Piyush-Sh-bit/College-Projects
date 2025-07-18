# Generated by Django 4.2.7 on 2025-07-08 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_approved_doctor',
            field=models.BooleanField(default=False, help_text='Whether doctor account is approved'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('admin', 'Administrator')], default='patient', max_length=10),
        ),
    ]
