from django.db import models
import os
from dotenv import load_dotenv
import base64
import requests
from django.conf import settings
from django.utils import timezone
import json
POLICY_TYPES = (
    ('Payment', 'Payment'),
    ('Shipping', 'Shipping'),
    ('Return', 'Return'),
)

load_dotenv()

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
    
    def get_encoded_credentials():
        credentials = f'{os.environ.get("EBAY_CLIENT_ID")}:{os.environ.get("EBAY_CLIENT_SECRET")}'
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def get_ebay_user_token(authorization_code, encoded_credentials):
        load_dotenv()
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
        data = {'grant_type': 'authorization_code','code': authorization_code, 'redirect_uri': os.environ.get("EBAY_RUNAME")}
        return requests.post('https://api.ebay.com/identity/v1/oauth2/token', headers=headers, data=data)
    
    @staticmethod
    def set_ebay_user_token(request, response):
        response_data = response.json()
        ebay_credentials, created = EbayCredential.objects.get_or_create(company_ref=request.user.company)
        ebay_credentials.token = response_data['access_token']
        ebay_credentials.token_expiration = timezone.now() + timedelta(seconds=response_data['expires_in'])
        ebay_credentials.refresh_token = response_data['refresh_token']
        ebay_credentials.refresh_token_expiration = timezone.now() + timedelta(seconds=response_data['refresh_token_expires_in'])
        ebay_credentials.save()
        request.user.company.ebay_credentials = ebay_credentials
        request.user.company.save()
        return ebay_credentials


    
class EbayMarketplace(models.Model):
    marketplace = models.CharField(max_length=100, null=True, blank=True)
    tree_id = models.IntegerField(null=True, blank=True)
    tree_version = models.IntegerField(null=True, blank=True)
    expiration = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def get_ebay_marketplace_id():
        return 'EBAY_MOTORS_US'

class Request(models.Model):
    user = models.ForeignKey('Authentication.User', on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    url = models.CharField(max_length=1000, null=True, blank=True)
    body = models.TextField(max_length=10000, null=True, blank=True)
    response = models.TextField(max_length=10000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def body_json(self):
        import json
        try:
            return json.dumps(json.loads(self.body), indent=4)
        except:
            return self.body
