from django.db import models

# Create your models here.
class UploadTemplate(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    csv = models.FileField(upload_to='ebay_upload_template', null=True, blank=True)

class Upload(models.Model):
    user = models.ForeignKey('Authentication.User', on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    csv = models.FileField(upload_to='ebay_upload', null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)