# Generated by Django 4.2.6 on 2024-05-18 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_company_is_core_buyer'),
        ('dashboards', '0040_customer_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='core',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cores', to='company.company'),
        ),
    ]
