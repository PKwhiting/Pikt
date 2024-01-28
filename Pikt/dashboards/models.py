from django.db import models
from django.conf import settings
import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import MinLengthValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import random
import string

PART_GRADES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

PART_STATUS = (
    ('Listed', 'Listed'),
    ('Sold', 'Sold'),
    ('Removed', 'Removed'),
    ('Pending', 'Pending'),
    ('On Hold', 'On Hold'),
)

ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

# Create your models here.
class image(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class part(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    vehicle_year = models.IntegerField()
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_trim = models.CharField(max_length=50)
    vehicle_engine = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    fitment_location = models.CharField(max_length=255)
    grade = models.CharField(max_length=1, choices=PART_GRADES)
    hollander_interchange = models.CharField(max_length=5000)
    notes = models.CharField(max_length=255)
    weight = models.IntegerField(null=True, blank=True) # in ounces
    height = models.IntegerField(null=True, blank=True) # in inches
    width = models.IntegerField(null=True, blank=True) # in inches
    length = models.IntegerField(null=True, blank=True) # in inches
    status = models.CharField(max_length=50, choices=PART_STATUS, default='Pending')
    vehicle_fitment = models.CharField(max_length=500)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    part_image_1 = models.ImageField(upload_to='images/', null=True, blank=True)
    part_image_2 = models.ImageField(upload_to='images/', null=True, blank=True)
    part_image_3 = models.ImageField(upload_to='images/', null=True, blank=True)
    part_image_4 = models.ImageField(upload_to='images/', null=True, blank=True)
    part_image_5 = models.ImageField(upload_to='images/', null=True, blank=True)
    part_image_6 = models.ImageField(upload_to='images/', null=True, blank=True)
    part_image_7 = models.ImageField(upload_to='images/', null=True, blank=True)
    part_image_8 = models.ImageField(upload_to='images/', null=True, blank=True)
    part_image_9 = models.ImageField(upload_to='images/', null=True, blank=True)
    part_image_10 = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    ebay_link = models.CharField(max_length=255, null=True, blank=True)
    sku = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, null=True, blank=True)
    def __str__(self):
        return f'{self.vehicle_year} {self.vehicle_make} {self.vehicle_model} {self.vehicle_trim} {self.vehicle_engine} {self.type}'
        

class Order(models.Model):
    sku = models.CharField(max_length=36)
    part_object = models.ForeignKey(part, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    shipping_label = models.FileField(upload_to='shipping_labels/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new object
            try:
                selected_part = part.objects.get(sku=self.sku)
                self.part_object = selected_part
            except part.DoesNotExist:
                pass

        super(Order, self).save(*args, **kwargs)