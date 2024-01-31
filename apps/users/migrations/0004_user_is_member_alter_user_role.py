# Generated by Django 4.1.6 on 2023-02-06 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_user', '0003_user_passport_image_path_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_member',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('unemployed', 'Unemployed'), ('office_manager', 'Office Manager'), ('agent', 'Agent'), ('manager', 'Manager'), ('delivery', 'Delivery')], default='delivery', max_length=400, null=True),
        ),
    ]
