# Generated by Django 3.2.23 on 2024-06-20 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0002_alter_invoice_destination'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
