# Generated by Django 4.2.6 on 2024-02-24 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_location_latitude_location_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='layout',
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
    ]
