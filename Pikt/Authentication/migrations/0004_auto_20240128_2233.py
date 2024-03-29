# Generated by Django 3.2.23 on 2024-01-28 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_remove_company_main_contact'),
        ('Authentication', '0003_auto_20240122_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='company.company'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_main_comany_contact',
            field=models.BooleanField(default=False),
        ),
    ]
