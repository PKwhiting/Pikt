# Generated by Django 3.2.23 on 2024-06-12 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0005_remove_vehicle_stock_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]
