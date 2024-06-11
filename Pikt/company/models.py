from django.db import models

STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)
# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=100, blank=True)
    address_line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True)
    zip_code = models.CharField(max_length=12, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    logo = models.ImageField(upload_to='company_logos', null=True, blank=True)
    website = models.CharField(max_length=100, blank=True)
    is_core_buyer = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Location(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField("Location Name", max_length=1024, blank=True, null=True)
    address1 = models.CharField("Address line 1", max_length=1024, blank=True, null=True)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField("ZIP / Postal code", max_length=12, blank=True, null=True)
    city = models.CharField("City", max_length=1024, blank=True, null=True)
    state = models.CharField("State", max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    layout = models.CharField(max_length=100000, null=True, blank=True)

class ShippingAddress(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField("Full name", max_length=1024)
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField("ZIP / Postal code", max_length=12)
    city = models.CharField("City", max_length=1024)

class BillingAddress(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField("Full name", max_length=1024)
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField("ZIP / Postal code", max_length=12)
    city = models.CharField("City", max_length=1024)







