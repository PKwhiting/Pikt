# Generated by Django 3.2.23 on 2024-06-28 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PartEbayCategorySpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_type', models.CharField(blank=True, max_length=100, null=True)),
                ('ebay_category', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
