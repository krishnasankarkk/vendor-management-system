# Generated by Django 5.0.4 on 2024-05-06 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_vendor_average_response_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_code',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]