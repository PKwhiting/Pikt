# Generated by Django 5.0.1 on 2024-01-21 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0009_rename_part_interchange_part_hollander_interchange_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='part_notes',
            new_name='notes',
        ),
    ]
