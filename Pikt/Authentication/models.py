from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from company.models import Location

ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Manager', 'Manager'),
    ('Employee', 'Employee'),
)

class funnelSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    yard_size = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=100)
    message = models.TextField()
    def __str__(self):
        return self.name


class User(AbstractUser):
    icon = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\d{3}-\d{3}-\d{4}$',
        message="Phone number must be entered in the format: '999-999-9999'"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True)  # validators should be a list
    messages = models.TextField(blank=True, default='[]')
    ebay_user_token = models.CharField(max_length=3000, blank=True)
    ebay_user_refresh_token = models.CharField(max_length=3000, blank=True)
    ebay_application_token = models.CharField(max_length=3000, blank=True)
    ebay_user_token_expiration = models.DateTimeField(null=True, blank=True)
    ebay_user_refresh_token_expiration = models.DateTimeField(null=True, blank=True)
    ebay_application_token_expiration = models.DateTimeField(null=True, blank=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    is_main_company_contact = models.BooleanField(default=False)
    role = models.CharField(choices=ROLE_CHOICES, max_length=10, default='Employee')
    u_pull_it_account = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='users')

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
