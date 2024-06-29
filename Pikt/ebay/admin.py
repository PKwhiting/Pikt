from django.contrib import admin
from .models import UploadTemplate, Upload, EbayPolicy, EbayCredential, EbayMarketplace
# Register your models here.
admin.site.register(UploadTemplate)
admin.site.register(Upload)
admin.site.register(EbayPolicy)
admin.site.register(EbayCredential)
admin.site.register(EbayMarketplace)