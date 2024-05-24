from django.contrib import admin
from .models import image
from .models import part
from .models import Order
from .models import Vehicle
from .models import Inventory
from .models import core
from .models import Customer

# Register your models here.
admin.site.register(image)
admin.site.register(part)
admin.site.register(Order)
admin.site.register(Vehicle)
admin.site.register(Inventory)
admin.site.register(core)
admin.site.register(Customer)