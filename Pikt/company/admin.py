from django.contrib import admin
from .models import Company
from .models import Location
from .models import ShippingAddress
from .models import BillingAddress
# Register your models here.

admin.site.register(Company)
admin.site.register(Location)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
