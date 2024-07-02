from datetime import timedelta
from django.db import models
import os
from dotenv import load_dotenv
import base64
import requests
from django.conf import settings
from django.utils import timezone
import json
from django.http import JsonResponse

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
    token = models.CharField(max_length=5000, null=True, blank=True)
    token_expiration = models.DateTimeField(null=True, blank=True)
    refresh_token = models.CharField(max_length=5000, null=True, blank=True)
    refresh_token_expiration = models.DateTimeField(null=True, blank=True)
    fulfillment_policy = models.ForeignKey(EbayPolicy, on_delete=models.CASCADE, null=True, blank=True, related_name='fulfillment_policy')
    payment_policy = models.ForeignKey(EbayPolicy, on_delete=models.CASCADE, null=True, blank=True, related_name='payment_policy')
    return_policy = models.ForeignKey(EbayPolicy, on_delete=models.CASCADE, null=True, blank=True, related_name='return_policy')

    
    def get_encoded_credentials():
        credentials = f'{os.environ.get("EBAY_CLIENT_ID")}:{os.environ.get("EBAY_CLIENT_SECRET")}'
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def get_ebay_user_tokens(authorization_code):
        response = EbayCredential.getUserToken(authorization_code)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['access_token'], response_data['refresh_token'], response_data['expires_in'], response_data['refresh_token_expires_in']
        else:
            return None, None, None, None
    
    @staticmethod
    def getUserToken(authorization_code):
        encoded_credentials = EbayCredential.get_encoded_credentials()
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
        data = {'grant_type': 'authorization_code','code': authorization_code, 'redirect_uri': os.environ.get("EBAY_RUNAME")}
        return requests.post('https://api.ebay.com/identity/v1/oauth2/token', headers=headers, data=data)
    
    @staticmethod
    def create_ebay_credentials(request, authorization_code):
        user_token, refresh_token, expires_in, refresh_token_expires_in = EbayCredential.get_ebay_user_tokens(authorization_code)
        if user_token and refresh_token and expires_in and refresh_token_expires_in:
            if not request.user.company.ebay_credentials:
                ebay_credentials = EbayCredential(token=user_token, refresh_token=refresh_token)
            else:
                ebay_credentials = request.user.company.ebay_credentials
                ebay_credentials.token = user_token
                ebay_credentials.refresh_token = refresh_token
            ebay_credentials.token_expiration = timezone.now() + timedelta(seconds=expires_in)
            ebay_credentials.refresh_token_expiration = timezone.now() + timedelta(seconds=refresh_token_expires_in)
            ebay_credentials.save()

            return ebay_credentials
        else:
            return None
    
    @staticmethod
    def set_company_ebay_credentials(request, authorization_code):
        ebay_credentials = EbayCredential.create_ebay_credentials(request, authorization_code)
        if ebay_credentials:
            request.user.company.ebay_credentials = ebay_credentials
            request.user.company.save()
            return ebay_credentials
        else:
            return None
    
    @staticmethod
    def get_credentials(user):
        credentials = user.company.ebay_credentials
        if not credentials:
            raise Exception("Ebay credentials not found")
        return credentials
    
    @classmethod
    def set_policies(cls, user, ebay_credentials):
        try:
            ebay_credentials.fulfillment_policy = get_first_fulfillment_policies(user)
            ebay_credentials.payment_policy = get_first_payment_policies(user)
            ebay_credentials.return_policy = get_first_return_policies(user)
            ebay_credentials.save()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False}, status=400)


    
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


def get_first_fulfillment_policies(user):
    marketplace_id = EbayMarketplace.get_ebay_marketplace_id()
    url = f"https://api.ebay.com/sell/account/v1/fulfillment_policy?marketplace_id={marketplace_id}"
    credentials = EbayCredential.get_credentials(user)
    headers =  {
            'Authorization': f'Bearer {credentials.token}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        if json_data['fulfillmentPolicies']:
            fulfillment_policy_id = json_data['fulfillmentPolicies'][0]['fulfillmentPolicyId']
            fulfillment_policy_name = json_data['fulfillmentPolicies'][0]['name']
            fulfillment_policy = EbayPolicy(company = user.company, policy_name=fulfillment_policy_name, policy_id=fulfillment_policy_id,  policy_type = POLICY_TYPES[1][0])
            fulfillment_policy.save()
            return fulfillment_policy
        else:
            raise Exception("Fulfillment policy was not found or does not exist.")
    else:
        raise Exception("Fulfillment policy was not found or does not exist.")
    
def get_first_payment_policies(user):
    marketplace_id = EbayMarketplace.get_ebay_marketplace_id()
    url = f"https://api.ebay.com/sell/account/v1/payment_policy?marketplace_id={marketplace_id}"
    credentials = EbayCredential.get_credentials(user)
    headers =  {
            'Authorization': f'Bearer {credentials.token}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        if json_data['paymentPolicies']:
            payment_policy_id = json_data['paymentPolicies'][0]['paymentPolicyId']
            payment_policy_name = json_data['paymentPolicies'][0]['name']
            payment_policy = EbayPolicy(company = user.company, policy_name=payment_policy_name, policy_id=payment_policy_id,  policy_type = POLICY_TYPES[0][0])
            payment_policy.save()
            return payment_policy
        else:
            raise Exception("Payment policy was not found or does not exist.")
    else:
        raise Exception("Payment policy was not found or does not exist.")
    
def get_first_return_policies(user):
    marketplace_id = EbayMarketplace.get_ebay_marketplace_id()
    url = f"https://api.ebay.com/sell/account/v1/return_policy?marketplace_id={marketplace_id}"
    credentials = EbayCredential.get_credentials(user)
    headers =  {
            'Authorization': f'Bearer {credentials.token}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        if json_data['returnPolicies']:
            return_policy_id = json_data['returnPolicies'][0]['returnPolicyId']
            return_policy_name = json_data['returnPolicies'][0]['name']
            return_policy = EbayPolicy(company = user.company, policy_name=return_policy_name, policy_id=return_policy_id,  policy_type = POLICY_TYPES[2][0])
            return_policy.save()
            return return_policy
        else:
            raise Exception("Return policy was not found or does not exist.")
    else:
        raise Exception("Return policy was not found or does not exist.")