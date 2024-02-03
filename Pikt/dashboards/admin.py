from django.contrib import admin
from .models import image
from .models import part
from .models import Order
from .models import Vehicle

# Register your models here.
admin.site.register(image)
admin.site.register(part)
admin.site.register(Order)
admin.site.register(Vehicle)