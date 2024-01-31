# Generated by Django 4.1.6 on 2023-07-09 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('file_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_number', models.CharField(blank=True, max_length=255, null=True)),
                ('create_contract_number', models.DateTimeField(blank=True, null=True)),
                ('inn', models.CharField(max_length=300)),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('total_price', models.FloatField(blank=True, null=True)),
                ('type_price', models.CharField(blank=True, max_length=300, null=True)),
                ('finished', models.BooleanField(default=False)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_address', models.CharField(blank=True, max_length=500, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=500, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_manager_send', models.BooleanField(blank=True, default=False, null=True)),
                ('created_date', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('price', models.FloatField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ManyToManyField(related_name='order_products', through='order.OrderItem', to='product.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_address', models.CharField(blank=True, max_length=500, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=500, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('inn', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]