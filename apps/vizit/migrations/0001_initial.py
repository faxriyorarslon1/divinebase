# Generated by Django 4.1.6 on 2024-01-17 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apps_user', '0068_version_checkmp_created_at_checkmp_district_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VizitExcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('path', models.FileField(blank=True, null=True, upload_to='excel_utils')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apps_user.district')),
            ],
        ),
        migrations.CreateModel(
            name='Vizit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('comment', models.CharField(max_length=1000)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_vizit', to='apps_user.city')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='district_vizit_all', to='apps_user.district')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_vizit', to='apps_user.doctor')),
                ('lpu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_vizit', to='apps_user.hospital')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_vizit', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
