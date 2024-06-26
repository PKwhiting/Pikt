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
        from ebay.utils import get_ebay_application_token, get_ebay_user_token, set_ebay_user_token, get_encoded_credentials
        load_dotenv()
        print(request)
        authorization_code = request.GET.get('code')
        expires_in = request.GET.get('expires_in')

        encoded_credentials = get_encoded_credentials()
        response = get_ebay_user_token(authorization_code, encoded_credentials)
        if response.status_code == 200:
            set_ebay_user_token(request, response)
            add_user_message(request, "Ebay integration complete")
        else:
            add_user_message(request, "Ebay consent failed")
        return redirect('dashboard')