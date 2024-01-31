# Generated by Django 4.1.6 on 2023-02-08 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_user', '0008_alter_city_district_alter_location_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=400)),
                ('last_name', models.CharField(max_length=400)),
                ('father_name', models.CharField(max_length=400)),
                ('phone_number', models.CharField(max_length=400)),
                ('type_doctor', models.CharField(max_length=400)),
                ('category_doctor', models.CharField(max_length=400)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('unemployed', 'Unemployed'), ('office_manager', 'Office Manager'), ('agent', 'Agent'), ('manager', 'Manager'), ('delivery', 'Delivery')], default='delivery', max_length=400, null=True),
        ),
    ]