from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_customuser_is_approved_doctor_alter_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='assigned_doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='accounts.customuser', limit_choices_to={'role': 'doctor'}),
        ),
    ]
