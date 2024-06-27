# import requests and os
import requests
import os
import json
from django.utils import timezone
from datetime import datetime, timedelta
from ebay.models import EbayCredential
from dotenv import load_dotenv
import base64

def add_user_message(request, message):
    messages = json.loads(request.user.messages)
    messages.append(message)
    request.user.messages = json.dumps(messages)
    request.user.save()

def get_encoded_credentials():
    load_dotenv()
    credentials = f'{os.environ.get("EBAY_CLIENT_ID")}:{os.environ.get("EBAY_CLIENT_SECRET")}'
    return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')


def get_ebay_user_token(authorization_code, encoded_credentials):
    load_dotenv()
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
    data = {'grant_type': 'authorization_code','code': authorization_code, 'redirect_uri': os.environ.get("EBAY_RUNAME")}
    return requests.post('https://api.ebay.com/identity/v1/oauth2/token', headers=headers, data=data)

def set_ebay_user_token(request, response):
    load_dotenv()
    response_data = response.json()
    ebay_credentials, created = EbayCredential.objects.get_or_create(company=request.user.company)
    ebay_credentials.token = response_data['access_token']
    ebay_credentials.token_expiration = timezone.now() + timedelta(seconds=response_data['expires_in'])
    ebay_credentials.refresh_token = response_data['refresh_token']
    ebay_credentials.refresh_token_expiration = timezone.now() + timedelta(seconds=response_data['refresh_token_expires_in'])
    ebay_credentials.save()

def get_ebay_application_token(authorization_code, encoded_credentials):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
    data = {'grant_type': 'client_credentials'}
    return requests.post('https://api.ebay.com/identity/v1/oauth2/token', headers=headers, data=data)

def handle_user_token(user):
    if datetime.now() >= user.token_expiration:
        if user.ebay_user_refresh_token:
            update_user_token(user)
        else:
            add_user_message(user, "Ebay token expired and no refresh token available")

def update_user_token(request):
    load_dotenv()
    encoded_credentials = get_encoded_credentials()
    refresh_token = request.user.ebay_user_refresh_token
    response = get_ebay_user_token_from_refresh_token(refresh_token, encoded_credentials)
    if response.status_code == 200:
        handle_user_success_response(request.user, response)
    else:
        add_user_message(request, "Ebay token refresh failed")

def get_ebay_user_token_from_refresh_token(refresh_token, encoded_credentials):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
    data = {'grant_type': 'refresh_token','refresh_token': refresh_token}
    return requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data)

def handle_user_success_response(user, response):
    ebay_credentials, create = EbayCredential.objects.get_or_create(company=user.company)
    response_data = response.json()
    ebay_credentials.token = response_data['access_token']
    ebay_credentials.token_expiration = timezone.now() + timedelta(seconds=response_data['expires_in'])
    ebay_credentials.refresh_token = response_data['refresh_token']
    ebay_credentials.refresh_token_expiration = timezone.now() + timedelta(seconds=response_data['refresh_token_expires_in'])
    ebay_credentials.save()
    add_user_message(user, "Ebay integration complete")

def get_credentials(user):
        credentials = EbayCredential.objects.filter(company=user.company).first()
        if not credentials:
            raise Exception("Ebay credentials not found")
        return credentials

def refresh_user_token(request):
    print("REFRESHING USER TOKEN")
    load_dotenv()
    credentials = get_credentials(request.user)
    if credentials.token_expiration <= timezone.now():
        if credentials.refresh_token:
            update_user_token(request)
        else:
            add_user_message(request, "Please re-authenticate your ebay credentials")

