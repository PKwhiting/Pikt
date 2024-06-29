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
    policy_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.company.name + ' - ' + self.policy_type)

class EbayMIPCredentials(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)

# make  a model that stores ebay credentials:
class EbayCredential(models.Model):
    company_ref = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    token = models.CharField(max_length=5000, null=True, blank=True)
    token_expiration = models.DateTimeField(null=True, blank=True)
    refresh_token = models.CharField(max_length=5000, null=True, blank=True)
    refresh_token_expiration = models.DateTimeField(null=True, blank=True)
    fulfillment_policy = models.ForeignKey(EbayPolicy, on_delete=models.CASCADE, null=True, blank=True, related_name='fulfillment_policy')
    payment_policy = models.ForeignKey(EbayPolicy, on_delete=models.CASCADE, null=True, blank=True, related_name='payment_policy')
    return_policy = models.ForeignKey(EbayPolicy, on_delete=models.CASCADE, null=True, blank=True, related_name='return_policy')

    def __str__(self):
        return str(self.company_ref.name)
    
class EbayMarketplace(models.Model):
    marketplace = models.CharField(max_length=100, null=True, blank=True)
    tree_id = models.IntegerField(null=True, blank=True)
    tree_version = models.IntegerField(null=True, blank=True)
    expiration = models.DateTimeField(null=True, blank=True)

class Request(models.Model):
    user = models.ForeignKey('Authentication.User', on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    url = models.CharField(max_length=1000, null=True, blank=True)
    body = models.TextField(max_length=10000, null=True, blank=True)
    response = models.TextField(max_length=10000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
