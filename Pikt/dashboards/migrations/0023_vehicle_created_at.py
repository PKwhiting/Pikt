# Generated by Django 3.2.23 on 2024-02-02 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0022_alter_part_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]