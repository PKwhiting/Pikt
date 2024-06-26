from django.db import models

POLICY_TYPES = (
    ('Payment', 'Payment'),
    ('Shipping', 'Shipping'),
    ('Return', 'Return'),
)

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

    def __str__(self):
        date_format = "%m-%d-%y %I:%M %p"
        return str(f'{self.user.username} - {self.company.name} - CREATED AT: {self.created_at.strftime(date_format)}')

class EbayPolicy(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    policy_type  = models.CharField(max_length=100, choices=POLICY_TYPES)
    policy_name = models.CharField(max_length=100, null=True, blank=True)

class EbayMIPCredentials(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)

# make  a model that stores ebay credentials:
class EbayCredential(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    token = models.CharField(max_length=1000, null=True, blank=True)
    token_expiration = models.DateTimeField(null=True, blank=True)
    refresh_token = models.CharField(max_length=1000, null=True, blank=True)
    refresh_token_expiration = models.DateTimeField(null=True, blank=True)
