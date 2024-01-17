# Generated by Django 5.0.1 on 2024-01-17 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0002_part_ebay_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='sellers_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
