from dotenv import load_dotenv
import base64
import requests
import os
import json
from datetime import datetime, timedelta
from django.utils import timezone


def handle_user_token(user):
    if datetime.now() >= user.token_expiration:
        if user.ebay_user_refresh_token:
            update_user_token(user)
        else:
            add_user_message(user, "Ebay token expired and no refresh token available")

# def handle_application_token(user):

def update_user_token(user):
    load_dotenv()
    encoded_credentials = get_encoded_credentials()
    refresh_token = user.ebay_user_refresh_token
    response = get_ebay_user_token_from_refresh_token(refresh_token, encoded_credentials)
    if response.status_code == 200:
        handle_user_success_response(user, response)
    else:
        add_user_message(user, "Ebay token refresh failed")

def get_ebay_user_token_from_refresh_token(refresh_token, encoded_credentials):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
    data = {'grant_type': 'refresh_token','refresh_token': refresh_token}
    return requests.post(os.environ.get("EBAY_TOKEN_URL"), headers=headers, data=data)

def get_encoded_credentials(self):
    credentials = f'{os.environ.get("EBAY_CLIENT_ID")}:{os.environ.get("EBAY_CLIENT_SECRET")}'
    return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

def set_user_token_expiration(user, response_data):
    now = timezone.now()
    user.ebay_user_token_expiration = now + timedelta(seconds=response_data['expires_in'])
    user.save()

def add_user_message(user, message):
    messages = json.loads(user.messages)
    messages.append(message)
    user.messages = json.dumps(messages)
    user.save()

def handle_user_success_response(user, response):
    response_data = response.json()
    user.ebay_user_token = response_data['access_token']
    set_user_token_expiration(user, response_data)


