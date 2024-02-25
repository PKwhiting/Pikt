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
    def __str__(self):
        return self.name

class part(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
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
    part_object = models.ForeignKey(part, on_delete=models.PROTECT, null=True, blank=True)
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

class Vehicle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    vin = models.CharField(max_length=17, null=True, blank=True)
    stock_number = models.CharField(max_length=256)
    year = models.IntegerField(blank=True, null=True)
    make = models.CharField(max_length=256, blank=True, null=True)
    model = models.CharField(max_length=256, blank=True, null=True)
    trim = models.CharField(max_length=256, blank=True, null=True)
    primary_damage = models.CharField(max_length=256, blank=True, null=True)
    secondary_damage = models.CharField(max_length=256, blank=True, null=True)
    yard = models.CharField(max_length=256, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True)
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

    def __str__(self):
        return self.stock_number