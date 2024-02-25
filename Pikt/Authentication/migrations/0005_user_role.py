# Generated by Django 3.2.23 on 2024-01-28 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0004_auto_20240128_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Employee', 'Employee')], default='Employee', max_length=10),
        ),
    ]