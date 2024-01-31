# Generated by Django 4.1.6 on 2023-02-08 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps_user', '0012_alter_user_role_agreedoctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreedoctor',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('unemployed', 'Unemployed'), ('office_manager', 'Office Manager'), ('agent', 'Agent'), ('manager', 'Manager'), ('delivery', 'Delivery')], default='delivery', max_length=400, null=True),
        ),
    ]