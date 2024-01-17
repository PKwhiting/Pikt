from django.contrib import admin
from .models import templateImage
from .models import templateIcon
from .models import User

# Register your models here.
admin.site.register(templateImage)
admin.site.register(templateIcon)
admin.site.register(User)
