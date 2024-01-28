# Generated by Django 3.2.23 on 2024-01-28 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20240128_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='address',
        ),
        migrations.RemoveField(
            model_name='location',
            name='manager',
        ),
        migrations.AddField(
            model_name='location',
            name='address1',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 1'),
        ),
        migrations.AddField(
            model_name='location',
            name='address2',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 2'),
        ),
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='location',
            name='name',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Full name'),
        ),
        migrations.AddField(
            model_name='location',
            name='zip_code',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='ZIP / Postal code'),
        ),
        migrations.AlterField(
            model_name='location',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
