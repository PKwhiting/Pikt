# Generated by Django 5.0.1 on 2024-01-21 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0007_rename_part_fitment_location_part_fitment_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='part_grade',
            new_name='grade',
        ),
    ]