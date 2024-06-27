from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EbayPolicy
import json
from dashboards.models import Part
from .models import UploadTemplate, Upload
import os
from django.conf import settings
from .const import PRODUCT_COMBINED_FIELDS
from dashboards.const.const import PARTS_CATEGORY_DICT
import csv
from django.http import HttpResponse
from .utils import add_user_message, get_ebay_application_token, get_ebay_user_token, set_ebay_user_token, get_encoded_credentials
from dotenv import load_dotenv
import base64
from django.contrib.auth import get_user_model
from company.models import Company
import requests
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import EbayCredential
from .serializers import InventoryItemSerializer, BulkInventoryItemSerializer
from django.utils import timezone

User = get_user_model()

class EbayAPIBaseView(APIView):
    url = None
    serializer = None
    success_message = None
    failure_message = None
    def get_credentials(self, user):
        credentials = EbayCredential.objects.filter(company=user.company).first()
        if not credentials:
            raise Exception("Ebay credentials not found")
        return credentials

    def refresh_token(self, credentials):
        url = "https://api.ebay.com/identity/v1/oauth2/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': credentials.refresh_token,
            'scope': 'https://api.ebay.com/oauth/api_scope/sell.inventory'
        }
        auth = (settings.EBAY_APP_ID, settings.EBAY_CERT_ID)

        response = requests.post(url, headers=headers, data=payload, auth=auth)
        if response.status_code == 200:
            data = response.json()
            credentials.token = data['access_token']
            credentials.token_expiration = timezone.now() + timezone.timedelta(seconds=data['expires_in'])
            credentials.save()
            return True
        return False

    def get_headers(self, credentials):
        if credentials.token_expiration <= timezone.now():
            if not self.refresh_token(credentials):
                raise Exception("Failed to refresh token")
        return {
            'Authorization': f'Bearer {credentials.token}',
            'Content-Language': 'en-US',
            'Content-Type': 'application/json'
        }

    def make_request(self, method, request, query):
        credentials = self.get_credentials(request.user)
        headers = self.get_headers(credentials)
        serializer = self.serializer(query)
        data = serializer.data
        response = requests.request(method, self.url, headers=headers, json=data)

        if response.status_code in [200, 201, 207]:
            if self.success_message:
                add_user_message(request, self.success_message)
        else:
            if self.failure_message:
                add_user_message(request, self.failure_message)

        return response


class SaveEbayPoliciesView(LoginRequiredMixin, View):
    def post(self, request):
        company = request.user.company
        success = True
        messages = []

        policy_types = request.POST.getlist('policy_type')
        policy_names = request.POST.getlist('policy_name')

        for policy_type, policy_name in zip(policy_types, policy_names):
            if policy_name:
                ebay_policy, created = EbayPolicy.objects.get_or_create(
                    company=company,
                    policy_type=policy_type,
                    defaults={'policy_name': policy_name}
                )
                if not created:
                    ebay_policy.policy_name = policy_name
                    ebay_policy.save()
            else:
                success = False

        if success:
            add_user_message(request, 'All policies saved successfully.')
        else:
            add_user_message(request, 'Some policies could not be saved.')

        return redirect('account')  # Redirect to an appropriate view after processing

class SetPartsEbayListedView(LoginRequiredMixin, View):
    def post(self, request):
        part_ids = request.POST.getlist('part_ids')
        if part_ids:
            parts = Part.objects.filter(id__in=part_ids)

            for part in parts:
                part.ebay_listed = True
                part.save()
        return redirect('parts')
    
class EbayDataFeedView(LoginRequiredMixin, View):
    def post(self, request):
        add_user_message(request, 'Data feed no longer supported')
        return redirect('parts')
    
class RedirectView(View):
    def get(self, request):
        load_dotenv()
        authorization_code = request.GET.get('code')
        encoded_credentials = get_encoded_credentials()
        response = get_ebay_user_token(authorization_code, encoded_credentials)
        if response.status_code == 200:
            set_ebay_user_token(request, response)
            add_user_message(request, "Ebay integration complete")
        else:
            add_user_message(request, "Ebay consent failed")
        return redirect('dashboard')
    

class BulkCreateOrReplaceInventoryItemView(EbayAPIBaseView):
    url = 'https://api.ebay.com/sell/inventory/v1/bulk_create_or_replace_inventory_item'
    serializer = BulkInventoryItemSerializer
    success_message = "Inventory uploaded to Ebay successfully"
    failure_message = "Failed to upload inventory to Ebay"

    def post(self, request):
        part_ids = request.POST.getlist('part_ids')
        if not part_ids:
            return Response({"error": "part_ids are required"}, status=status.HTTP_400_BAD_REQUEST)

        parts = Part.objects.filter(id__in=part_ids)
        if not parts.exists():
            return Response({"error": "No parts found with the given IDs"}, status=status.HTTP_404_NOT_FOUND)

        self.make_request('POST', request, query=parts)

        return redirect('parts')

from .serializers import BulkEbayOfferDetailsWithKeysSerializer
class BulkCreateOffersView(EbayAPIBaseView):
    url = 'https://api.ebay.com/sell/inventory/v1/bulk_publish_offers'
    serializer = BulkEbayOfferDetailsWithKeysSerializer
    success_message = "Offers published to Ebay successfully"
    failure_message = "Failed to publish offers to Ebay"

    def post(self, request):
        part_ids = request.POST.getlist('part_ids')
        if not part_ids:
            return Response({"error": "part_ids are required"}, status=status.HTTP_400_BAD_REQUEST)

        parts = Part.objects.filter(id__in=part_ids)
        if not parts.exists():
            return Response({"error": "No parts found with the given IDs"}, status=status.HTTP_404_NOT_FOUND)

        self.make_request('POST', request, query=parts)

        return redirect('parts')














