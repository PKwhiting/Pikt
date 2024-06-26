# import requests and os
import requests
import os
import json
from django.utils import timezone
from datetime import datetime, timedelta
from ebay.models import EbayCredentials
from dotenv import load_dotenv
import base64

def add_user_message(request, message):
    messages = json.loads(request.user.messages)
    messages.append(message)
    request.user.messages = json.dumps(messages)
    request.user.save()

def get_encoded_credentials(self):
    load_dotenv()
    credentials = f'{os.environ.get("EBAY_CLIENT_ID")}:{os.environ.get("EBAY_CLIENT_SECRET")}'
    return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')


def get_ebay_user_token(self, authorization_code, encoded_credentials):
    load_dotenv()
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
    data = {'grant_type': 'authorization_code','code': authorization_code, 'redirect_uri': os.environ.get("EBAY_RUNAME")}
    return requests.post('https://api.ebay.com/identity/v1/oauth2/token', headers=headers, data=data)

def set_ebay_user_token(self, request, response):
    load_dotenv()
    response_data = response.json()
    ebay_credentials = EbayCredentials.objects.get_or_create(company=request.user.company)
    ebay_credentials.token = response_data['access_token']
    ebay_credentials.token_expiration = timezone.now() + timedelta(seconds=response_data['expires_in'])
    ebay_credentials.refresh_token = response_data['refresh_token']
    ebay_credentials.refresh_token_expiration = timezone.now() + timedelta(seconds=response_data['refresh_token_expires_in'])
    ebay_credentials.save()
    add_user_message(request, "Ebay integration complete")

def get_ebay_application_token(self, authorization_code, encoded_credentials):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
    data = {'grant_type': 'client_credentials'}
    return requests.post('https://api.ebay.com/identity/v1/oauth2/token', headers=headers, data=data)