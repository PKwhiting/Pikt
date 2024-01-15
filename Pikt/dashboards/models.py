from django.db import models
from django.contrib.auth.models import User

PART_GRADES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

PART_STATUS = (
    ('Listed', 'Listed'),
    ('Sold', 'Sold'),
    ('Removed', 'Removed'),
    ('Shipped', 'Shipped'),
    ('Pending', 'Pending'),
    ('On Hold', 'On Hold'),
)

# Create your models here.
class image(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class part(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vehicle_year = models.IntegerField()
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_trim = models.CharField(max_length=50)
    vehicle_engine = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=50)
    part_type = models.CharField(max_length=50)
    part_fitment_location = models.CharField(max_length=255)
    part_grade = models.CharField(max_length=1, choices=PART_GRADES)
    part_interchange = models.CharField(max_length=50)
    part_notes = models.CharField(max_length=255)
    part_status = models.CharField(max_length=50, choices=PART_STATUS, default='Pending')
    vehicle_fitment = models.CharField(max_length=500)
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
    def __str__(self):
        return f'{self.vehicle_year} {self.vehicle_make} {self.vehicle_model} {self.vehicle_trim} {self.vehicle_engine} {self.part_type}'
        