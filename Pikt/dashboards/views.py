from django.shortcuts import render, redirect
from django.views import View
from .models import part
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PartForm
from django.core.paginator import Paginator
import base64
import json
import os
from django.conf import settings
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from urllib.parse import unquote
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.db.models import Avg
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .const.const import PARTS_CONST, MAKES_MODELS
from django.db import IntegrityError
import requests
from urllib.parse import urlencode
from django.http import HttpResponseRedirect

context = {
    'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
    'years' : range(2024, 1969, -1),
    'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
    'makes': ['AMC', 'Acura', 'Alfa', 'Audi', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler','Daewoo', 'Daihatsu', 'Dodge', 'Eagle', 'Fiat', 'Ford', 'GMC', 'Genesis', 'Geo', 'Honda', 'Hummer', 'Hyundai', 'IH', 'Infiniti', 'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Land Rover', 'Lexus', 'Lincoln', 'Maserati', 'Mazda', 'McLaren', 'Mercedes', 'Mercury', 'MG', 'Mini', 'Mitsubishi', 'Nissan', 'Oldsmobile', 'Pagani', 'Peugeot', 'Plymouth', 'Pontiac', 'Porsche', 'Ram', 'Renault', 'Rivian', 'Rover', 'Saab', 'Saturn', 'Scion', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Triumph', 'Volkswagen', 'Volvo']
}

class delete_message(View):
    def post(self, request):
        if request.method == 'POST':
            message_to_delete = request.POST.get('message')
            messages = json.loads(request.user.messages)
            for message in messages:
                if message_to_delete == message:
                    messages.remove(message_to_delete)
            request.user.messages = json.dumps(messages)
            request.user.save()
            previous_page = request.META.get('HTTP_REFERER')
            return redirect(previous_page)

class rootView(LoginRequiredMixin,View):
    def get(self, request):
        parts = part.objects.filter(user=request.user).order_by('-created_at')[:5]
        # get the price of all parts from the user that have a status of 'sold'
        sold_parts = part.objects.filter(user=request.user, status='Sold')
        total_revenue = round(sold_parts.aggregate(Sum('price'))['price__sum'], 2) if sold_parts.aggregate(Sum('price'))['price__sum'] is not None else '0.00'
        shipped_parts = part.objects.filter(user=request.user, status='Shipped')
        unsold_parts = part.objects.filter(user=request.user, status__in=['Pending', 'Listed'])
        average_price = unsold_parts.aggregate(Avg('price'))['price__avg'] if unsold_parts.aggregate(Avg('price'))['price__avg'] is not None else '0.00'
        last_12_months = []
        for i in range(7, -1, -1):
            last_12_months.append((datetime.now() - relativedelta(months=i)).strftime('%B'))

        inventory_by_month = []
        for i in range(7, -1, -1):
            date = datetime.now() - relativedelta(months=i)
            month_name = date.strftime('%B')
            month_number = date.month
            inventory_by_month.append({
                'month': month_name,
                'total_sales': unsold_parts.filter(created_at__month=month_number).aggregate(total_sales=Coalesce(Sum('price'), Decimal('0.00')))['total_sales']
            })
        inventory_by_month = ["{:.2f}".format(float(item['total_sales'])) for item in inventory_by_month]

        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'messages': json.loads(request.user.messages),
            'parts': parts,
            'sold_parts': sold_parts.count(),
            'shipped_parts': shipped_parts.count(),
            'total_revenue': total_revenue,
            'average_price': round(average_price,2) if average_price != '0.00' else '0.00',
            'last_12_months': json.dumps(last_12_months),
            'inventory_by_month': inventory_by_month,
        }


        return render(request, 'dashboard.html', context)
 
class defaultDashboardView(LoginRequiredMixin,View):
    def get(self, request):
        parts = part.objects.filter(user=request.user) if request.user.is_authenticated else []
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'parts': parts,
            'messages':json.loads(request.user.messages)
        }
        if context['parts'].count() > 0:
            parts_list = part.objects.filter(user=request.user)
            paginator = Paginator(parts_list, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['parts'] = page_obj
        return render(request, 'parts.html', context)

@login_required  
def add_part(request):
    if request.method == 'POST':
        post = request.POST.copy()  # Make a mutable copy
        fitment_location = request.POST.getlist('fitment_location')
        post['fitment_location'] = json.dumps(fitment_location)
        form = PartForm(post, request.FILES)
        if form.is_valid():
            part = form.save(commit=False)
            part.user = request.user
            images = request.FILES.getlist('images')
            for i in range(1, min(11, len(images) + 1)):
                image_field = f'part_image_{i}'
                setattr(part, image_field, images[i-1])
            form.save()
            messages = json.loads(request.user.messages)
            messages.append('Part added successfully')
            request.user.messages = json.dumps(messages)
            request.user.save()
            return redirect('/dashboards/parts')  # Redirect to a page showing all parts
        else:
            context['form'] = form
            messages = json.loads(request.user.messages)
            messages.append('Part was not added')
            request.user.messages = json.dumps(messages)
            request.user.save()
    else:
        form = PartForm()
    context = {
        'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
        'years' : range(2024, 1969, -1),
        'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
        'makes_models': MAKES_MODELS,
        'form': form,
        'messages': json.loads(request.user.messages),
        'part_types': PARTS_CONST,
    
    }
    context['form'] = form
    context['messages'] = json.loads(request.user.messages)
    return render(request, 'add-part.html', context)

@login_required
def delete_part(request, part_id):
    part_to_delete = get_object_or_404(part, id=part_id)
    try:
        part_to_delete.delete()
    except IntegrityError:
        messages = json.loads(request.user.messages)
        messages.append('This part cannot be deleted because it is being used elsewhere')
        request.user.messages = json.dumps(messages)
        request.user.save()
        return redirect('single_part', part_id=part_id)
    messages = json.loads(request.user.messages)
    messages.append('Part deleted successfully')
    request.user.messages = json.dumps(messages)
    request.user.save()
    return redirect('/dashboards/')

class single_part(LoginRequiredMixin, View):
    def get(self, request, part_id=None, *args, **kwargs):
        selected_part = get_object_or_404(part, id=part_id)
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'messages': json.loads(request.user.messages),
            'part': selected_part,
            'potential_profit': selected_part.price - selected_part.cost,
            'roi': round((selected_part.price - selected_part.cost) / selected_part.cost * 100, 2)
        }
        return render(request, 'single-part.html', context)

class ebayConsent(View):
    def get(self, request):
        consent_url = "https://auth.sandbox.ebay.com/oauth2/authorize?client_id=PKWhitin-Pikt-SBX-ee5696659-e1c11b44&response_type=code&redirect_uri=PK_Whiting-PKWhitin-Pikt-S-glbjhb&scope=https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/buy.order.readonly https://api.ebay.com/oauth/api_scope/buy.guest.order https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.marketplace.insights.readonly https://api.ebay.com/oauth/api_scope/commerce.catalog.readonly https://api.ebay.com/oauth/api_scope/buy.shopping.cart https://api.ebay.com/oauth/api_scope/buy.offer.auction https://api.ebay.com/oauth/api_scope/commerce.identity.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.email.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.phone.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.address.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.name.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.status.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/sell.item.draft https://api.ebay.com/oauth/api_scope/sell.item https://api.ebay.com/oauth/api_scope/sell.reputation https://api.ebay.com/oauth/api_scope/sell.reputation.readonly https://api.ebay.com/oauth/api_scope/commerce.notification.subscription https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly https://api.ebay.com/oauth/api_scope/sell.stores https://api.ebay.com/oauth/api_scope/sell.stores.readonly"
        return HttpResponseRedirect(consent_url)

class RedirectView(View):
    def get(self, request):
        load_dotenv()
        authorization_code = request.GET.get('code')
        # authorization_code = "v^1.1#i^1#f^0#r^1#p^3#I^3#t^Ul41Xzg6Qzc5Qzc0ODdCMkEwMkFEODk5RDA4RTM1OTA4QkQ3RDdfMl8xI0VeMTI4NA=="
        # print(f'Basic {authorization_code}')
        credentials = f'{os.getenv("CLIENT_ID")}:{os.getenv("CLIENT_SECRET")}'
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        url = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
        data = {'grant_type': 'authorization_code','code': authorization_code, 'redirect_uri': 'PK_Whiting-PKWhitin-Pikt-S-glbjhb'}

        response = requests.post(url, headers=headers, data=data)

        response_data = response.json()
        access_token = response_data['access_token']
        expires_in = response_data['expires_in']
        token_type = response_data['token_type']
        messages = json.loads(request.user.messages)
        messages.append(f'{access_token} {expires_in} {token_type}')
        messages.append(response)
        request.user.messages = json.dumps(messages)
        request.user.save()
        return render(request, 'dashboard.html', context)