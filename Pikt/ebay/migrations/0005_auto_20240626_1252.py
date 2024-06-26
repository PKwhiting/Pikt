# Generated by Django 3.2.23 on 2024-06-26 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebay', '0004_auto_20240626_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebaycredentials',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ebaycredentials',
            name='refresh_token_expiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ebaycredentials',
            name='token',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]