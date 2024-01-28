from django.shortcuts import render, redirect
from django.views import View
from .models import part, Order
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PartForm
from django.core.paginator import Paginator
import base64
import json
import os
import ast
from django.conf import settings
from django.utils import timezone
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
from decimal import Decimal
from .const.const import PARTS_CONST, MAKES_MODELS
from django.db import IntegrityError
import requests
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

context = {
    'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
    'years' : range(2024, 1969, -1),
    'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
    'makes': ['AMC', 'Acura', 'Alfa', 'Audi', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler','Daewoo', 'Daihatsu', 'Dodge', 'Eagle', 'Fiat', 'Ford', 'GMC', 'Genesis', 'Geo', 'Honda', 'Hummer', 'Hyundai', 'IH', 'Infiniti', 'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Land Rover', 'Lexus', 'Lincoln', 'Maserati', 'Mazda', 'McLaren', 'Mercedes', 'Mercury', 'MG', 'Mini', 'Mitsubishi', 'Nissan', 'Oldsmobile', 'Pagani', 'Peugeot', 'Plymouth', 'Pontiac', 'Porsche', 'Ram', 'Renault', 'Rivian', 'Rover', 'Saab', 'Saturn', 'Scion', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Triumph', 'Volkswagen', 'Volvo']
}
def add_user_message(request, message):
    messages = json.loads(request.user.messages)
    messages.append(message)
    request.user.messages = json.dumps(messages)
    request.user.save()

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
        parts = part.objects.filter(user=request.user).order_by('-created_at')[:3]
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
            part.vehicle_fitment = form.cleaned_data['vehicle_fitment']
            part.weight = form.cleaned_data['weight']
            part.user = request.user
            part.save()
            form.save()
            messages = json.loads(request.user.messages)
            messages.append('Part added successfully')
            request.user.messages = json.dumps(messages)
            request.user.save()
            return redirect('/dashboards/parts')  # Redirect to a page showing all parts
        else:
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

def edit_part(request, part_id):
    part_instance = get_object_or_404(part, id=part_id)

    # if saving edits toa part
    if request.method == 'POST':
        form = PartForm(request.POST, request.FILES, instance=part_instance)
        if form.is_valid():
            part_instance = form.save(commit=False)

            # converting python object string to python object
            current_fitments = ast.literal_eval(part_instance.vehicle_fitment)
            current_key = int(list(current_fitments.keys())[-1])

            # if there are existing fitments add to existing object else set fitment equal to new fitment(s)
            if len(part_instance.vehicle_fitment) > 2:
                for key, new_fitment in form.cleaned_data['vehicle_fitment'].items():
                    current_key += 1
                    current_fitments[f'{current_key}'] = new_fitment
                part_instance.vehicle_fitment = current_fitments
            else:
                part_instance.vehicle_fitment = form.cleaned_data['vehicle_fitment']

            # set part weight and user
            part_instance.weight = form.cleaned_data['weight']
            part_instance.user = request.user
            part_instance.save()
            form.save()
            add_user_message(request, 'Part updated successfully')
            return redirect('/dashboards/parts')  # Redirect to the parts list
        else:
            add_user_message(request, 'Part was not updated')
    else:
        form = PartForm(instance=part_instance)

    if part_instance.vehicle_fitment:
        vehicle_fitments = ast.literal_eval(part_instance.vehicle_fitment)
    else:
        vehicle_fitments = {}
    fitment_list = [(index, fitment) for index, fitment in vehicle_fitments.items()]
    context = {
        'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
        'years' : range(2024, 1969, -1),
        'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
        'makes_models': MAKES_MODELS,
        'form': form,
        'part': part_instance,
        'messages': json.loads(request.user.messages),
        'part_types': PARTS_CONST,
        'form': form,
        'messages': json.loads(request.user.messages),
        'part_lbs' : part_instance.weight // 16 if part_instance.weight is not None else None,
        'part_ozs' : part_instance.weight % 16 if part_instance.weight is not None else None,
        'vehicle_fitments': fitment_list,
    }
    return render(request, 'edit-part.html', context)

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
            'potential_profit': (selected_part.price or Decimal('0.01')) - (selected_part.cost or Decimal('0.01')),
            'roi': round(((selected_part.price or Decimal('0.01')) - (selected_part.cost or Decimal('0.01'))) / (selected_part.cost or Decimal('0.01')) * 100, 2)   
        }
        return render(request, 'single-part.html', context)
    
class orders(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all()
        shipped_orders = Order.objects.filter(status='Shipped')
        processing_orders = Order.objects.filter(status='Processing')
        cancelled_orders = Order.objects.filter(status='Cancelled')
        total_revenue = round(orders.aggregate(Sum('price'))['price__sum'], 2) if orders.aggregate(Sum('price'))['price__sum'] is not None else '0.00'
        total_orders = Order.objects.count() or 0
        deliveries = Order.objects.filter(status='Delivered') or 0
        unique_customer_count = Order.objects.values_list('customer_name', flat=True).distinct().count() or 0
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'orders': orders,
            'revenue': total_revenue,
            'total_orders': total_orders,
            'deliveries': deliveries,
            'messages':json.loads(request.user.messages),
            'unique_customer_count': unique_customer_count,
            'shipped_orders': shipped_orders,
            'processing_orders': processing_orders,
            'cancelled_orders': cancelled_orders,
        }
        return render(request, 'orders.html', context)





class ebayConsent(View):
    def get(self, request):
        consent_url = "https://auth.ebay.com/oauth2/authorize?client_id=PKWhitin-Pikt-PRD-be5696659-6f69cb6d&response_type=code&redirect_uri=PK_Whiting-PKWhitin-Pikt-P-wnidgnd&scope=https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/commerce.identity.readonly https://api.ebay.com/oauth/api_scope/sell.reputation https://api.ebay.com/oauth/api_scope/sell.reputation.readonly https://api.ebay.com/oauth/api_scope/commerce.notification.subscription https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly https://api.ebay.com/oauth/api_scope/sell.stores https://api.ebay.com/oauth/api_scope/sell.stores.readonly"
        return HttpResponseRedirect(consent_url)

class RedirectView(View):
    def get(self, request):
        load_dotenv()
        authorization_code = request.GET.get('code')
        encoded_credentials = self.get_encoded_credentials()

        response = self.get_ebay_user_token(authorization_code, encoded_credentials)

        if response.status_code == 200:
            self.handle_success_response(request, response)
        else:
            add_user_message(request, "Ebay consent failed")

        context['messages'] = json.loads(request.user.messages)
        return redirect('dashboard')

    def get_encoded_credentials(self):
        credentials = f'{os.environ.get("EBAY_CLIENT_ID")}:{os.environ.get("EBAY_CLIENT_SECRET")}'
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    def get_ebay_user_token(self, authorization_code, encoded_credentials):
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
        data = {'grant_type': 'authorization_code','code': authorization_code, 'redirect_uri': os.environ.get("EBAY_RUNAME")}
        return requests.post(os.environ.get("EBAY_TOKEN_URL"), headers=headers, data=data)
    
    def get_ebay_application_token(self, authorization_code, encoded_credentials):
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_credentials}'}
        data = {'grant_type': 'client_credentials'}
        return requests.post(os.environ.get("EBAY_TOKEN_URL"), headers=headers, data=data)


    def handle_success_response(self, request, response):
        response_data = response.json()
        request.user.ebay_user_token = response_data['access_token']
        request.user.ebay_user_refresh_token = response_data['refresh_token']
        self.set_token_expiration(request, response_data)
        add_user_message(request, "Ebay integration complete")

    def set_token_expiration(self, request, response_data):
        now = timezone.now()
        request.user.ebay_user_token_expiration = now + timedelta(seconds=response_data['expires_in'])
        request.user.ebay_user_refresh_token_expiration = now + timedelta(seconds=response_data['refresh_token_expires_in'])
        request.user.save()

    def add_user_message(self, request, message):
        messages = json.loads(request.user.messages)
        messages.append(message)
        request.user.messages = json.dumps(messages)
        request.user.save()