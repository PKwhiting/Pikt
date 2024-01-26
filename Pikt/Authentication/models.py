from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from dotenv import load_dotenv
import base64
import requests
import os
import json
from datetime import datetime, timedelta
from django.utils import timezone

class User(AbstractUser):
    icon = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\d{3}-\d{3}-\d{4}$',
        message="Phone number must be entered in the format: '999-999-9999'"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True)  # validators should be a list
    messages = models.TextField(blank=True, default='[]')
    ebay_user_token = models.CharField(max_length=3000, blank=True)
    ebay_user_refresh_token = models.CharField(max_length=3000, blank=True)
    ebay_application_token = models.CharField(max_length=3000, blank=True)
    ebay_user_token_expiration = models.DateTimeField(null=True, blank=True)
    ebay_user_refresh_token_expiration = models.DateTimeField(null=True, blank=True)
    ebay_application_token_expiration = models.DateTimeField(null=True, blank=True)

    def handle_tokens(self):
        #if user ebay token is expired 
        print(timezone.now())
        print(self.ebay_user_token_expiration)
        if timezone.now() > self.ebay_user_token_expiration:
            print("TACOS")
            # if user refresh token is not expired
            if timezone.now() > self.ebay_user_refresh_token_expiration:
                update_user_token(self)

            # else if user refresh token is expired
            else:
                self.ebay_user_token == ""
                add_user_message(self, "Please go to account settings to refresh your ebay token")
                return False
        else:
            return True

class templateImage(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class templateIcon(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
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



