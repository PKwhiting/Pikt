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
from .ftp_client import FTPClient

def add_user_message(request, message):
    messages = json.loads(request.user.messages)
    messages.append(message)
    request.user.messages = json.dumps(messages)
    request.user.save()

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
        part_ids = request.POST.getlist('part_ids')
        if part_ids:
            parts = Part.objects.filter(id__in=part_ids)
            
            upload_template = UploadTemplate.objects.get(name="PRODUCT_COMBINED")
            template_file_path = upload_template.csv.path

            # Read the template file and prepare the filled CSV file
            filled_csv_file_path = os.path.join(settings.MEDIA_ROOT, 'filled_product_combined.csv')

            with open(template_file_path, 'r') as template_file, open(filled_csv_file_path, 'w', newline='') as filled_csv_file:
                reader = csv.DictReader(template_file)
                writer = csv.DictWriter(filled_csv_file, fieldnames=PRODUCT_COMBINED_FIELDS.keys())
                writer.writeheader()

                for part in parts:
                    row = PRODUCT_COMBINED_FIELDS.copy()
                    row.update({
                        'SKU': part.stock_number,
                        'Localized For': 'en_US',
                        'Title': part.type,
                        'Product Description': part.description if part.description != '' else part.type,
                        'Condition': 'USED_EXCELLENT' if part.grade == 'A' else 'USED_VERY_GOOD' if part.grade == 'B' else 'USED_GOOD' if part.grade == 'C' else 'USED_ACCEPTABLE',
                        'List Price': part.price,
                        'Total Ship To Home Quantity': 1,
                        'Shipping Policy': EbayPolicy.objects.get(company=request.user.company, policy_type='Shipping').policy_name,
                        'Payment Policy': EbayPolicy.objects.get(company=request.user.company, policy_type='Payment').policy_name,
                        'Return Policy': EbayPolicy.objects.get(company=request.user.company, policy_type='Return').policy_name,
                        'Attribute Name 1': 'Part Grade',
                        'Attribute Value 1': part.grade,
                        'Category': PARTS_CATEGORY_DICT[part.type],
                        'Picture URL 1': 'data:image/jpeg;base64,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',
                        'Picture URL 2': part.image_2.url if part.image_2 else '',
                        'Picture URL 3': part.image_3.url if part.image_3 else '',
                        'Picture URL 4': part.image_4.url if part.image_4 else '',
                        'Picture URL 5': part.image_5.url if part.image_5 else '',
                        'Picture URL 6': part.image_6.url if part.image_6 else '',
                        'Picture URL 7': part.image_7.url if part.image_7 else '',
                        'Picture URL 8': part.image_8.url if part.image_8 else '',
                        'Picture URL 9': part.image_9.url if part.image_9 else '',
                        'Picture URL 10': part.image_10.url if part.image_10 else '',
                    })
                    writer.writerow(row)
            upload_instance = Upload.objects.create(user=request.user, company=request.user.company, status='FILLED', csv='filled_product_combined.csv')
            upload_instance.save()

            try:
                ftp_client = FTPClient('mip.ebay.com', 'whi-521217', 'v^1.1#i^1#f^0#r^1#d^2024-12-21T13:30:24.161Z#p^3#I^3#t^Ul4xMF84OjdCNkUyMzkzQUM0RkJENjFGN0YzRDZCOTNGQTg1QzdDXzBfMSNFXjI2MA==', port=2222)
                ftp_client.connect()
                print(ftp_client.list_directories('/store/config-spec/'))
                print(ftp_client.list_files('/store/config-spec/'))
                print("----")
                print(ftp_client.list_files('/store/lookup/'))
                # ftp_client.upload_file(filled_csv_file_path, '/store/product/filled_product_combined.csv')
                ftp_client.close()

                add_user_message(request, 'Parts uploaded successfully.')
            except Exception as e:
                add_user_message(request, f'Error uploading parts to Ebay: {str(e)}')
            
            return redirect('parts')

        else:
            return redirect('parts')