# Generated by Django 3.2.23 on 2024-06-26 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebay', '0003_ebaycredentials_ebaymipcredentials'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebaycredentials',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ebaycredentials',
            name='token_expiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
