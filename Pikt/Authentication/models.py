from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator

class User(AbstractUser):
    icon = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\d{3}-\d{3}-\d{4}$',
        message="Phone number must be entered in the format: '999-999-9999'"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True)  # validators should be a list
    messages = models.TextField(blank=True, default='[]')

class templateImage(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class templateIcon(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
