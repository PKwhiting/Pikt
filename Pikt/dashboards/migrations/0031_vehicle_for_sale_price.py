# Generated by Django 4.2.6 on 2024-02-25 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0030_vehicle_marker'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='for_sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
