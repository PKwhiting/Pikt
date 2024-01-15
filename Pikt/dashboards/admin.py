from django.contrib import admin
from .models import image
from .models import part

# Register your models here.
admin.site.register(image)
admin.site.register(part)