# Generated by Django 3.2.23 on 2024-01-28 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0005_user_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_main_comany_contact',
            new_name='is_main_company_contact',
        ),
    ]