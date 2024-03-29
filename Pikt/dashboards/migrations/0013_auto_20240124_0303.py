# Generated by Django 3.2.23 on 2024-01-24 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0012_rename_part_type_part_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='height',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='length',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='weight',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='width',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='part',
            name='hollander_interchange',
            field=models.CharField(max_length=5000),
        ),
    ]
