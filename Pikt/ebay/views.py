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
import sentry_sdk
from sentry_sdk import capture_exception
from parts.models import PartEbayCategorySpecification
from .utils import EbayAPIRequestView, refresh_user_token, get_get_headers, get_post_headers, get_category_tree_id, get_category_suggestions, get_location_id, get_first_fulfillment_policies, get_first_payment_policies, get_first_return_policies, delete_ebay_item_offer
from .serializers import BulkEbayOfferDetailsWithKeysSerializer, BulkPublishOfferRequestSerializer
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

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
            ebay_credentials = set_ebay_user_token(request, response)
            add_user_message(request, "Ebay integration complete")
        else:
            add_user_message(request, "Ebay consent failed")
            return redirect('dashboard')

        # create the ebay policies
        try:
            response = get_first_fulfillment_policies(request.user)
            if response is not None:
                fulfillment_policy_id, fulfillment_policy_name = response
                shipping_policy, create = EbayPolicy.objects.get_or_create(
                    company=request.user.company, 
                    policy_type='Shipping',   
                )
                shipping_policy.policy_name=fulfillment_policy_name, 
                shipping_policy.policy_id=fulfillment_policy_id
                shipping_policy.save()
                ebay_credentials.fulfillment_policy = shipping_policy
                ebay_credentials.save()
                
            else:
                add_user_message(request, "Ebay shipping policies not found")
        except Exception as e:
            capture_exception(e)

        try:
            response = get_first_payment_policies(request.user)
            if response is not None:
                payment_policy_id, payment_policy_name = response
                payment_policy, create = EbayPolicy.objects.get_or_create(
                    company=request.user.company, 
                    policy_type='Payment',   
                )
                payment_policy.policy_name=payment_policy_name
                payment_policy.policy_id=payment_policy_id
                payment_policy.save()
                ebay_credentials.payment_policy = payment_policy
                ebay_credentials.save()
            else:
                add_user_message(request, "Ebay payment policies not found")
        except Exception as e:
            capture_exception(e)

        try:
            response = get_first_return_policies(request.user)
            if response is not None:
                return_policy_id, return_policy_name = response
                return_policy, create = EbayPolicy.objects.get_or_create(
                    company=request.user.company, 
                    policy_type='Return',   
                )
                return_policy.policy_name=return_policy_name
                return_policy.policy_id=return_policy_id
                return_policy.save()
                ebay_credentials.return_policy = return_policy
                ebay_credentials.save()
            else:
                add_user_message(request, "Ebay return policies not found")
        except Exception as e:
            capture_exception(e)
        
        if not request.user.company.ebay_merchant_location_key:
            location_id = get_location_id(request.user)
            request.user.company.ebay_merchant_location_key = location_id
            request.user.company.save()

        return redirect('dashboard')
    

class BulkCreateOrReplaceInventoryItemView(EbayAPIRequestView):
    url = 'https://api.ebay.com/sell/inventory/v1/bulk_create_or_replace_inventory_item'
    serializer = BulkInventoryItemSerializer
    success_message = "Inventory uploaded to Ebay successfully"
    failure_message = "Failed to upload inventory to Ebay"

    def post(self, request, query=None):
        self.query = query
        return self.make_request('POST', request)

class BulkCreateOffersView(EbayAPIRequestView):
    url = 'https://api.ebay.com/sell/inventory/v1/bulk_create_offer'
    serializer = BulkEbayOfferDetailsWithKeysSerializer
    success_message = "Offers published to Ebay successfully"
    failure_message = "Failed to publish offers to Ebay"

    def post(self, request, query=None):
        for part in query:
            if part.ebay_category_id == '' or not part.ebay_category_id:
                specification, create = PartEbayCategorySpecification.objects.get_or_create(part_type=part.type)
                if create:
                    specification.ebay_category_id = get_category_suggestions(request.user, part.type)
                    specification.save()
                    part.ebay_category_id = specification.ebay_category_id
                    part.save()
                else:
                    part.ebay_category_id = specification.ebay_category_id
                    part.save()

        self.query = query
        return self.make_request('POST', request)

class BulkPublishOffersView(EbayAPIRequestView):
    url = 'https://api.ebay.com/sell/inventory/v1/bulk_publish_offer'
    serializer = BulkPublishOfferRequestSerializer
    success_message = "Offers published to Ebay successfully"
    failure_message = "Failed to publish offers to Ebay"

    def post(self, request, query=None):
        self.query = query
        return self.make_request('POST', request)


class ListPartsView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            part_ids = self.get_part_ids(request)
            parts = self.get_parts(part_ids)

            # filter through the parts and remove the ones that are ebay_listed
            parts = parts.exclude(ebay_listed=True)

            if parts.count() == 0:
                logger.info("All parts are already listed")
                return redirect('parts')


            if not parts.exists():
                return self.error_response("No valid parts found", status=status.HTTP_404_NOT_FOUND)

            self.ensure_no_existing_offers(request, parts)

            self.process_inventory_items(request, parts)

            offers_response = self.process_offers(request, parts)

            self.update_parts_with_offer_ids(parts, offers_response.json())

            # reinitialize parts list with updated offer ids
            parts = self.get_parts(part_ids)
            self.publish_offers(request, parts)


            return redirect('parts')
        except ValueError as e:
            return self.error_response(str(e))
        except Exception as e:
            capture_exception(e)
            return self.error_response(f"An unexpected error occurred: {str(e)}")
            
        
    def get_part_ids(self, request):
        part_ids = request.POST.getlist('part_ids')
        if not part_ids:
            raise ValueError("part_ids are required")
        return part_ids

    def get_parts(self, part_ids):
        return Part.objects.filter(id__in=part_ids)
    
    def ensure_no_existing_offers(self, request, parts):
        for part in parts:
            if part.ebay_offer_id:
                delete_ebay_item_offer(request.user, part.ebay_offer_id)
                part.ebay_offer_id = None
                part.save()

    def process_inventory_items(self, request, parts):
        inventory_response = BulkCreateOrReplaceInventoryItemView().post(request, query=parts)
        if not self.is_successful_response(inventory_response):
            raise Exception("Failed to create inventory items")

    def process_offers(self, request, parts):
        offers_response = BulkCreateOffersView().post(request, parts)
        if not self.is_successful_response(offers_response):
            raise Exception("Failed to create offers")
        return offers_response

    def update_parts_with_offer_ids(self, parts, response_data):
        offers = [(response["sku"], response["offerId"]) for response in response_data["responses"]]
        skus = [sku for sku, _ in offers]
 
        for sku, offer_id in offers:
            part = parts.get(stock_number=sku)
            part.ebay_offer_id = offer_id
            part.save()


    def publish_offers(self, request, parts):
        publish_response = BulkPublishOffersView().post(request, parts)
        if self.is_successful_response(publish_response):
            for part in parts:
                part.ebay_listed = True
                part.save()
        if not self.is_successful_response(publish_response):
            raise Exception("Failed to publish offers")

    def is_successful_response(self, response):
        return response.status_code in [200, 201, 204]

    def error_response(self, message):
        add_user_message(self.request, message)
        return redirect('parts')












