# import requests and os
import requests
import os
import json
from django.utils import timezone
from datetime import datetime, timedelta
from ebay.models import EbayCredential, Request
from dotenv import load_dotenv
import base64
import requests
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import EbayCredential
import logging

logger = logging.getLogger(__name__)


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
    ebay_credentials, created = EbayCredential.objects.get_or_create(company_ref=request.user.company)
    ebay_credentials.token = response_data['access_token']
    ebay_credentials.token_expiration = timezone.now() + timedelta(seconds=response_data['expires_in'])
    ebay_credentials.refresh_token = response_data['refresh_token']
    ebay_credentials.refresh_token_expiration = timezone.now() + timedelta(seconds=response_data['refresh_token_expires_in'])
    ebay_credentials.save()
    request.user.company.ebay_credentials = ebay_credentials
    request.user.company.save()
    return ebay_credentials

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
        set_user_token(request.user, response)
    else:
        add_user_message(request, "Ebay token refresh failed")

def get_ebay_user_token_from_refresh_token(refresh_token, encoded_credentials):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
    data = {'grant_type': 'refresh_token','refresh_token': refresh_token}
    return requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data)

def set_user_token(user, response):
    ebay_credentials, create = EbayCredential.objects.get_or_create(company_ref=user.company)
    response_data = response.json()
    ebay_credentials.token = response_data['access_token']
    ebay_credentials.token_expiration = timezone.now() + timedelta(seconds=response_data['expires_in'])
    ebay_credentials.save()

# def handle_user_success_response(user, response):
#     ebay_credentials, create = EbayCredential.objects.get_or_create(company_ref=user.company)
#     response_data = response.json()
#     ebay_credentials.token = response_data['access_token']
#     ebay_credentials.token_expiration = timezone.now() + timedelta(seconds=response_data['expires_in'])
#     ebay_credentials.refresh_token = response_data['refresh_token']
#     ebay_credentials.refresh_token_expiration = timezone.now() + timedelta(seconds=response_data['refresh_token_expires_in'])
#     ebay_credentials.save()
#     add_user_message(user, "Ebay integration complete")

def get_credentials(user):
        credentials = EbayCredential.objects.filter(company_ref=user.company).first()
        if not credentials:
            raise Exception("Ebay credentials not found")
        return credentials

def refresh_user_token(request):
    load_dotenv()
    credentials = get_credentials(request.user)
    if credentials.token_expiration <= timezone.now():
        if credentials.refresh_token:
            update_user_token(request)
        else:
            add_user_message(request, "Please re-authenticate your ebay credentials")

def get_get_headers(user):
    credentials = get_credentials(user)
    return {
        'Authorization': f'Bearer {credentials.token}',
        'Content-Language': 'en-US',
        'Content-Type': 'application/json'
    }

def get_post_headers(user):
    credentials = get_credentials(user)
    return {
        'Authorization': f'Bearer {credentials.token}',
        'Content-Language': 'en-US',
        'Content-Type': 'application/json'
    }

from .models import EbayMarketplace
def get_marketplace_details(user, marketplace_id):
    url = f"https://api.ebay.com/commerce/taxonomy/v1/get_default_category_tree_id?marketplace_id={marketplace_id}"
    headers = get_get_headers(user)
    response = requests.get(url, headers=headers)
    response = response.json()
    return response['categoryTreeId'], response['categoryTreeVersion']

def get_ebay_marketplace_id():
    return 'EBAY_MOTORS_US'

def get_category_tree_id(user):
    marketplace_id = get_ebay_marketplace_id()
    ebay_marketplace = EbayMarketplace.objects.get(marketplace=marketplace_id)
    if ebay_marketplace.expiration <= timezone.now():
        ebay_marketplace.tree_id, ebay_marketplace.tree_version = get_marketplace_details(user, marketplace_id)
        ebay_marketplace.expiration = timezone.now() + timedelta(days=100)
        ebay_marketplace.save()
    return ebay_marketplace.tree_id

import json
import io
import zipfile
from django.http import HttpResponse
from django.views import View
def get_category_suggestions(user, query):
    category_tree_id = get_category_tree_id(user)
    url = f"https://api.ebay.com/commerce/taxonomy/v1/category_tree/{category_tree_id}/get_category_suggestions?q=car truck {query}"
    credentials = get_credentials(user)
    headers =  {
            'Authorization': f'Bearer {credentials.token}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }

    response = requests.get(url, headers=headers)
    json_data = response.json()
    
    first_category_id = json_data['categorySuggestions'][0]['category']['categoryId']
    return first_category_id

def get_location_id(user):
    url = "https://api.ebay.com/sell/inventory/v1/location?0&1"
    credentials = get_credentials(user)
    headers =  {
            'Authorization': f'Bearer {credentials.token}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    json_data = response.json()
    merchant_location_key = json_data["locations"][0]["merchantLocationKey"]
    return merchant_location_key


def get_first_fulfillment_policies(user):
    url = f"https://api.ebay.com/sell/account/v1/fulfillment_policy?marketplace_id=EBAY_MOTORS_US"
    credentials = get_credentials(user)
    headers =  {
            'Authorization': f'Bearer {credentials.token}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        fulfillment_policy_id = json_data['fulfillmentPolicies'][0]['fulfillmentPolicyId']
        fulfillment_policy_name = json_data['fulfillmentPolicies'][0]['name']
        return fulfillment_policy_id, fulfillment_policy_name
    else:
        return None

def get_first_payment_policies(user):
    url = f"https://api.ebay.com/sell/account/v1/payment_policy?marketplace_id=EBAY_MOTORS_US"
    credentials = get_credentials(user)
    headers =  {
            'Authorization': f'Bearer {credentials.token}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        payment_policy_id = json_data['paymentPolicies'][0]['paymentPolicyId']
        payment_policy_name = json_data['paymentPolicies'][0]['name']
        return payment_policy_id, payment_policy_name
    else:
        return None

def get_first_return_policies(user):
    url = f"https://api.ebay.com/sell/account/v1/return_policy?marketplace_id=EBAY_MOTORS_US"
    credentials = get_credentials(user)
    headers =  {
            'Authorization': f'Bearer {credentials.token}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        return_policy_id = json_data['returnPolicies'][0]['returnPolicyId']
        return_policy_name = json_data['returnPolicies'][0]['name']
        return return_policy_id, return_policy_name
    else:
        return None
    
def delete_ebay_item_offer(user, offer_id):
    url = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}"
    credentials = get_credentials(user)
    headers =  {
            'Authorization': f'Bearer {credentials.token}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")  # Log HTTP error
        raise Exception(f"Failed to delete offer {offer_id}: {http_err}")
    except requests.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")  # Log connection error
        raise Exception(f"Failed to delete offer {offer_id}: {conn_err}")
    except requests.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")  # Log timeout error
        raise Exception(f"Failed to delete offer {offer_id}: {timeout_err}")
    except requests.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")  # Log general request error
        raise Exception(f"Failed to delete offer {offer_id}: {req_err}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")  # Log any other unexpected errors
        raise Exception(f"An unexpected error occurred: {str(e)}")
    
    

class EbayAPIRequestView(APIView):
    url = None
    serializer = None
    success_message = None
    failure_message = None
    queryset = None
    request = None

    def get_credentials(self, user):
        credentials = EbayCredential.objects.filter(company_ref=user.company).first()
        if not credentials:
            logger.error("Ebay credentials not found")
            raise Exception("Ebay credentials not found")
        return credentials

    def get_headers(self, credentials):
        if not credentials or not credentials.token:
            logger.error("Invalid credentials")
            raise Exception("Invalid credentials")
        return {
            'Authorization': f'Bearer {credentials.token}',
            'Content-Language': 'en-US',
            'Content-Type': 'application/json'
        }

    def validate_query(self, query):
        if not query or not query.exists() or not query.count() > 0:
            logger.warning("Empty query")
            raise ValueError("Empty query")

    def prepare_data(self):
        if not self.serializer or not self.query:
            logger.error("Serializer or query not defined")
            raise Exception("Serializer or query not defined")
        serializer = self.serializer(self.query)
        if not serializer.data:
            logger.error("Invalid serializer data")
            raise ValueError("Invalid data")
        return serializer.data

    def handle_response_messages(self, response):
        if response.status_code in [200, 201, 207, 204]:
            if self.success_message:
                add_user_message(self.request, self.success_message)
        else:
            if self.failure_message:
                add_user_message(self.request, self.failure_message)
            response_data = response.json()
            errors = response_data.get('errors', [])
            for error in errors:
                logger.error(f"Error {error.get('errorId')}: {error.get('message')}")
            #     add_user_message(self.request, f"Error {error.get('errorId')}: {error.get('message')}")
            # raise Exception(f"API request failed with status code {response.status_code}")

    def construct_request(self, method, request, ebay_request_object):
        try:
            refresh_user_token(request)
            credentials = self.get_credentials(request.user)
            headers = self.get_headers(credentials)
            data = self.prepare_data()
            ebay_request_object.body = data
            ebay_request_object.save()
            response = requests.request(method, self.url, headers=headers, json=data)
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    def make_request(self, method, request):
        self.request = request
        try:
            self.validate_query(self.query)
            ebay_request_object = Request(user=request.user, company=request.user.company, url=self.url)
            ebay_request_object.save()
            response = self.construct_request(method, request, ebay_request_object)
            ebay_request_object.response = response.json()
            ebay_request_object.save()
            self.handle_response_messages(response)
            return response
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


