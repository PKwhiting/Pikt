from django.contrib import admin
from .models import UploadTemplate, Upload, EbayPolicy, EbayCredentials
# Register your models here.
admin.site.register(UploadTemplate)
admin.site.register(Upload)
admin.site.register(EbayPolicy)
admin.site.register(EbayCredentials)