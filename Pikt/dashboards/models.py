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
from company.models import Location

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

SELLER_TYPE = [
        ('COPART', 'COPART'),
        ('IAA', 'IAA'),
        ('Street', 'Street'),
        ('Charity', 'Charity'),
        ('Vendor', 'Vendor'),
    ]

# Create your models here.
class image(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50)

class Part(models.Model):
    stock_number = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True)
    vehicle = models.ForeignKey('dashboards.Vehicle', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=1, choices=PART_GRADES, null=True, blank=True)
    interchange = models.CharField(max_length=5000, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True) # in ounces
    height = models.IntegerField(null=True, blank=True) # in inches
    width = models.IntegerField(null=True, blank=True) # in inches
    length = models.IntegerField(null=True, blank=True) # in inches
    status = models.CharField(max_length=50, choices=PART_STATUS, default='Pending')
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    ebay_listed = models.BooleanField(default=False)
    mercari_listed = models.BooleanField(default=False)
    marketplace_listed = models.BooleanField(default=False)
    sold = models.BooleanField(default=False) 
    image_1 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_6 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_7 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_8 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_9 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_10 = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    
    
    @staticmethod
    def get_highest_stock_number():
        from django.db.models import Max
        highest_stock_number = Part.objects.aggregate(Max('stock_number'))['stock_number__max']
        if highest_stock_number is None:
            return 100500
        return int(highest_stock_number)

class Order(models.Model):
    sku = models.CharField(max_length=36)
    part_object = models.ForeignKey(Part, on_delete=models.PROTECT, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    shipping_label = models.FileField(upload_to='shipping_labels/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new object
            try:
                selected_part = Part.objects.get(sku=self.sku)
                self.part_object = selected_part
            except Part.DoesNotExist:
                pass

        super(Order, self).save(*args, **kwargs)

from company.models import Company
class Vehicle(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    vin = models.CharField(max_length=17, null=True, blank=True)
    year = models.IntegerField(blank=True, null=True)
    make = models.CharField(max_length=256, blank=True, null=True)
    model = models.CharField(max_length=256, blank=True, null=True)
    trim = models.CharField(max_length=256, blank=True, null=True)
    primary_damage = models.CharField(max_length=256, blank=True, null=True)
    secondary_damage = models.CharField(max_length=256, blank=True, null=True)
    yard = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    marker = models.CharField(max_length=10000, blank=True, null=True)
    row = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    engine = models.CharField(max_length=256, blank=True, null=True)
    mileage = models.CharField(max_length=256, blank=True, null=True)
    transmission = models.CharField(max_length=256, blank=True, null=True)
    body_type = models.CharField(max_length=256, blank=True, null=True)
    drivetrain = models.CharField(max_length=256, blank=True, null=True)
    exterior_primary_color = models.CharField(max_length=256, blank=True, null=True)
    exterior_primary_paint_code = models.CharField(max_length=256, blank=True, null=True)
    exterior_secondary_color = models.CharField(max_length=256, blank=True, null=True)
    exterior_secondary_paint_code = models.CharField(max_length=256, blank=True, null=True)
    interior_primary_color = models.CharField(max_length=256, blank=True, null=True)
    interior_primary_paint_code = models.CharField(max_length=256, blank=True, null=True)
    interior_secondary_color = models.CharField(max_length=256, blank=True, null=True)
    interior_secondary_paint_code = models.CharField(max_length=256, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    for_sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    auction_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    buyer_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    internet_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tow_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dismantler_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    storage_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pullout_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    misc_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    buyer = models.CharField(max_length=256, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    seller_type = models.CharField(max_length=256, choices=SELLER_TYPE, blank=True, null=True)
    seller_first_name = models.CharField(max_length=256, blank=True, null=True)
    seller_last_name = models.CharField(max_length=256, blank=True, null=True)
    seller_phone = models.CharField(max_length=256, blank=True, null=True)
    seller_email = models.EmailField(max_length=256, blank=True, null=True)
    seller_address = models.CharField(max_length=256, blank=True, null=True)
    seller_city = models.CharField(max_length=256, blank=True, null=True)
    seller_state = models.CharField(max_length=256, blank=True, null=True)
    possession_date = models.DateField(blank=True, null=True)
    cleared_date = models.DateField(blank=True, null=True)
    towed_by = models.CharField(max_length=256, blank=True, null=True)
    inventoried_date = models.DateField(blank=True, null=True)
    dismantled_by = models.CharField(max_length=256, blank=True, null=True)
    dismantled_date = models.DateField(blank=True, null=True)
    crush_date = models.DateField(blank=True, null=True)
    sold_date = models.DateField(blank=True, null=True)
    image_1 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_6 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_7 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_8 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_9 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_10 = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # Assuming images are handled with a separate model or method

class Inventory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    file = models.FileField(upload_to='inventory_files/')

class core(models.Model):
    interchange = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='cores')

    
class Customer(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='customers')

class PartPreference(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='part_preferences')
    parts = models.TextField(blank=True, help_text="Comma-separated list of parts")

    def get_parts_list(self):
        if self.parts:
            return self.parts.split(',')
        return []

    def set_parts_list(self, parts_list):
        self.parts = ','.join(parts_list)

