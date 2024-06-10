from django.contrib import admin
from .models import image
from .models import Part
from .models import Order
from .models import Vehicle
from .models import Inventory
from .models import core
from .models import Customer
from .models import PartPreference

# Register your models here.
admin.site.register(image)
admin.site.register(Part)
admin.site.register(Order)
admin.site.register(Vehicle)
admin.site.register(Inventory)
admin.site.register(core)
admin.site.register(Customer)
admin.site.register(PartPreference)