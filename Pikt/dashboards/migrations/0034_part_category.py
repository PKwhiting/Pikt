# Generated by Django 4.2.6 on 2024-05-17 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0033_part_stock_number_part_vehicle_vin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
