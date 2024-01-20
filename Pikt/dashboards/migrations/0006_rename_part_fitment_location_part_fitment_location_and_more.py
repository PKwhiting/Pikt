# Generated by Django 5.0.1 on 2024-01-20 23:46

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0005_rename_part_fitment_location_part_fitment_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
