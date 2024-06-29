from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Part, Order, Vehicle, Inventory, PartPreference
from company.models import Location
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PartForm
from .forms import VehicleForm
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
import base64
import json
from django.template.loader import render_to_string
import os
from django.http import HttpResponse
from django.db.models import Max
import ast
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
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
from .const.const import PARTS_CONST, MAKES_MODELS, DAMAGE_TYPE_CONST, CATEGORY_CONST, TRANSMISSION_CONST, COLORS_CONST, SELLER_TYPE_CONST, STATE_CHOICES
from django.db import IntegrityError
import requests
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models import Sum, DecimalField
from decimal import Decimal
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.views.decorators.http import require_POST
from .models import Customer
from django.db.models import Max, Sum, Subquery, OuterRef
from .models import core
import pdfkit
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import CustomerForm

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

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
        return redirect('vehicles')
 
from .forms import PartFilterForm
from ebay.models import UploadTemplate, EbayPolicy
import csv
from ebay.const import PRODUCT_COMBINED_FIELDS
from .const.const import PARTS_CATEGORY_DICT
from .models import PartImage

class defaultDashboardView(LoginRequiredMixin,View):
    def get(self, request):
        parts = Part.objects.filter(company=request.user.company)
        
        filter_form = PartFilterForm()
        unlisted_parts = parts.filter(
            ebay_listed=False,
            sold=False,
            part_images__isnull=False
        ).distinct()

        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years': range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'parts': parts,
            'unlisted_parts': unlisted_parts,
            'messages': json.loads(request.user.messages),
            'makes_models': MAKES_MODELS,
            'part_types': PARTS_CONST,
            'table_items': parts,
            'filterForm': filter_form,
            'item_action': 'single_part',
            'filter_form_action': reverse('filter_parts'),
            'filter_form_headers': list(filter_form.fields.keys()),
        }
        request.user.messages = []
        request.user.save()
        return render(request, 'parts.html', context)

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
                        'Picture URL 1': part.image_1.url if part.image_1 else '',
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
            
            # Return the filled CSV file as a download response
            with open(filled_csv_file_path, 'r') as filled_csv_file:
                response = HttpResponse(filled_csv_file, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="filled_product_combined.csv"'
                return response

        else:
            # Handle the case where no parts were selected.
            return redirect('parts')


class yardView(LoginRequiredMixin,View):
    def get(self, request):
        location = request.user.location
        vehicles = Vehicle.objects.filter(location=location).exclude(category="CRUSHED") if request.user.is_authenticated else []
        incomingVehicles = Vehicle.objects.filter(location=location, category='INCOMING') if request.user.is_authenticated else []
        categories = ['HOLDING', 'NO TITLE', 'NEEDS A STICKER', 'TITLE PROBLEM', 'VIN NOT IN SYSTEM', 'INCOMING']  # Add your categories here
        holdingVehicles = Vehicle.objects.filter(location=location, category__in=categories) if request.user.is_authenticated else []
        preStripVehicles = Vehicle.objects.filter(location=location, category='PRE DRAIN') if request.user.is_authenticated else []
        stripVehicles = Vehicle.objects.filter(location=location, category='DRAINING') if request.user.is_authenticated else []
        preYardVehicles = Vehicle.objects.filter(location=location, category='PRE YARD') if request.user.is_authenticated else []
        yardVehicles = Vehicle.objects.filter(location=location, category='YARD') if request.user.is_authenticated else []
        processingVehicles = Vehicle.objects.filter(location=location, category='PROCESSING') if request.user.is_authenticated else []
        forSaleVehicles = Vehicle.objects.filter(location=location, category='FOR SALE') if request.user.is_authenticated else []
        crushedVehicles = Vehicle.objects.filter(location=location, category='CRUSHED') if request.user.is_authenticated else []
        vehiclesList = json.dumps(list(vehicles.values()), cls=DjangoJSONEncoder)
        incomingVehiclesList = json.dumps(list(incomingVehicles.values()), cls=DjangoJSONEncoder)
        holdingVehiclesList = json.dumps(list(holdingVehicles.values()), cls=DjangoJSONEncoder)
        preStripVehiclesList = json.dumps(list(preStripVehicles.values()), cls=DjangoJSONEncoder)
        stripVehiclesList = json.dumps(list(stripVehicles.values()), cls=DjangoJSONEncoder)
        preYardVehiclesList = json.dumps(list(preYardVehicles.values()), cls=DjangoJSONEncoder)
        yardVehiclesList = json.dumps(list(yardVehicles.values()), cls=DjangoJSONEncoder)
        processingVehiclesList = json.dumps(list(processingVehicles.values()), cls=DjangoJSONEncoder)
        forSaleVehiclesList = json.dumps(list(forSaleVehicles.values()), cls=DjangoJSONEncoder)
        crushedVehiclesList = json.dumps(list(crushedVehicles.values()), cls=DjangoJSONEncoder)
        emptyVehicleSpots = location.layout if location else []
        vehiclesWithMarkers = list(Vehicle.objects.filter(location=location).exclude(marker__isnull=True).values())
        vehiclesWithMarkers_json = json.dumps(vehiclesWithMarkers, cls=DjangoJSONEncoder)
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years': range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'vehicles': vehicles,
            'vehiclesList': vehiclesList,
            'incomingVehicles': incomingVehicles,
            'incomingVehiclesList': incomingVehiclesList,
            'holdingVehiclesList': holdingVehiclesList,
            'preStripVehiclesList': preStripVehiclesList,
            'stripVehiclesList': stripVehiclesList,
            'preYardVehiclesList': preYardVehiclesList,
            'processingVehiclesList': processingVehiclesList,
            'forSaleVehiclesList': forSaleVehiclesList,
            'crushedVehiclesList': crushedVehiclesList,
            'holdingVehicles': holdingVehicles,
            'preStripVehicles': preStripVehicles,
            'stripVehicles': stripVehicles,
            'preYardVehicles': preYardVehicles,
            'yardVehicles': yardVehicles,
            'yardVehiclesList': yardVehiclesList,
            'processingVehicles': processingVehicles,
            'forSaleVehicles': forSaleVehicles,
            'crushedVehicles': crushedVehicles,
            'messages': json.loads(request.user.messages),
            'makes_models': MAKES_MODELS,
            'part_types': PARTS_CONST,
            'categories': CATEGORY_CONST,
            'emptyVehicleSpots': emptyVehicleSpots,
            'markedVehicles': vehiclesWithMarkers_json,
        }
        if context['vehicles'].count() > 0:
            vehicles = Vehicle.objects.filter(location=location).exclude(category="CRUSHED").order_by('id')
            paginator = Paginator(vehicles, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['vehicles'] = page_obj

        if is_ajax(request):
            requestType = request.headers['x-request-type']
            if requestType == 'vehicleEdit':
                vehicle_ids_string = request.GET.get('vehicleIds', '')
                vehicle_ids_list = vehicle_ids_string.split(',')
                location = request.GET.get('location')
                category = request.GET.get('category')
                row = request.GET.get('row')
                for vehicle_id in vehicle_ids_list:
                    vehicle_id = int(vehicle_id)
                    vehicle = Vehicle.objects.get(id=vehicle_id)
                    if location != '':
                        vehicle.location = location
                    if category != '':
                        vehicle.category = category
                    if row != '':
                        vehicle.row = row
                    vehicle.save()
            elif requestType == 'newVehicleLocation':
                selectedMarker = request.GET.get('selectedMarker')
                vehicle_id = request.GET.get('vehicleId')
                location = request.user.location
                vehicle = Vehicle.objects.get(id=vehicle_id)
                vehicle.location = location
                vehicle.marker = selectedMarker
                vehicle.save()
                selectedMarker = json.loads(selectedMarker)

                vehiclesWithMarkers = list(Vehicle.objects.filter(location=location).exclude(marker__isnull=True).values())
                add_user_message(request, 'Location updated successfully')
                return JsonResponse({'success': True, 'locationEmptySpots': location.layout, 'vehiclesWithMarkers': vehiclesWithMarkers}, safe=False)
            else:
                year_start = request.GET.get('year_start')
                year_end = request.GET.get('year_end')
                vehicle_make = request.GET.get('vehicle_make')
                vehicle_model = request.GET.get('vehicle_model')
                category = request.GET.get('category')
                vin = request.GET.get('vin')
                stock_number = request.GET.get('stock_number')

                vehicles = Vehicle.objects.filter(user=request.user)
                if year_start:
                    vehicles = vehicles.filter(year__gte=year_start)
                if year_end:
                    vehicles = vehicles.filter(year__lte=year_end)
                if vehicle_model:
                    vehicles = vehicles.filter(model__icontains=vehicle_model)
                if vehicle_make:
                    vehicles = vehicles.filter(make__icontains=vehicle_make)
                if category:
                    vehicles = vehicles.filter(category__iexact=category)
                if vin:
                    vehicles = vehicles.filter(vin__icontains=vin)
                if stock_number:
                    vehicles = vehicles.filter(stock_number__icontains=stock_number)
                context['vehicles'] = vehicles
                context['filtered_vehicles'] = vehicles
                if context['vehicles'].count() > 0:
                    vehicles = vehicles.order_by('id')
                    paginator = Paginator(vehicles, 20)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    context['vehicles'] = page_obj
                    context['year_start_filter'] = year_start
                    context['year_end_filter'] = year_end
                    context['vehicle_make_filter'] = vehicle_make
                    context['vehicle_model_filter'] = vehicle_model
                    context['category_filter'] = category
                    context['vin_filter'] = vin
                # html = render_to_string('vehicles-table.html', {'vehicles': vehicles}, request=request)
                # Constructing the response data
                response_data = {
                    'html': render_to_string('vehicles-table.html', context),
                    'vehicles': list(vehicles.values()),  # Assuming 'vehicles' is a QuerySet; adapt as needed
                }

                return JsonResponse(response_data)
                # return HttpResponse(render_to_string('vehicles-table.html', context))
        
        request.user.messages = []
        request.user.save()
        return render(request, 'vehiclesYard.html', context)

@login_required  
def add_part(request):
    if request.method == 'POST':
        post = request.POST.copy()  # Make a mutable copy
        fitment_location = request.POST.getlist('fitment_location')
        post['fitment_location'] = json.dumps(fitment_location)
        form = PartForm(post, request.FILES)
        if form.is_valid():
            part = form.save(commit=False)
            Part.vehicle_fitment = form.cleaned_data['vehicle_fitment']
            Part.weight = form.cleaned_data['weight']
            Part.user = request.user
            Part.save()
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
    request.user.messages = []
    request.user.save()
    return render(request, 'add-Part.html', context)

@login_required  
def add_vehicle(request):
    if request.method == 'POST':
        post = request.POST.copy()  # Make a mutable copy
        form = VehicleForm(post, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            form.save()
            add_user_message(request, 'Vehicle added successfully')
            return redirect('/dashboards/vehicles')  # Redirect to a page showing all parts
        else:
            messages = json.loads(request.user.messages)
            messages.append('Vehicle was not added, try again')
            request.user.messages = json.dumps(messages)
            request.user.save()
    elif is_ajax(request):
        requestType = request.headers['x-request-type']
        if requestType == 'multiVehicleUpload':
            vehicles = request.GET.get('vehicles')
            category = request.GET.get('category')
            vehicles_list = json.loads(vehicles)
            try:
                for vehicle in vehicles_list:
                    vin = vehicle.get("vin")
                    stock_number = vin[-6:]
                    vehicle = Vehicle(user=request.user ,vin=vehicle.get("vin"), year=vehicle.get("year"), make=vehicle.get("make"), model=vehicle.get("model"), category=category, location=request.user.location, stock_number=stock_number)
                    vehicle.save()
                add_user_message(request, 'Vehicles added successfully')
            except:
                add_user_message(request, 'Issue while adding vehicles. Try again.')
            return JsonResponse({'success': True}, safe=False)

        else:
            location_id = request.GET.get('location_id')   
            lat = Location.objects.get(id=location_id).latitude
            lng = Location.objects.get(id=location_id).longitude
            location = Location.objects.filter(latitude=lat, longitude=lng)[0]
            vehicles = Vehicle.objects.filter(location=location)
            vehicles_data = serialize('List', vehicles)
            vehicles_data_json = json.loads(vehicles_data)
            return JsonResponse({'lat': lat, 'lng': lng, 'vehicles': vehicles_data_json}, safe=False)

    else:
        form = VehicleForm()
    next_vehicle_id = Vehicle.objects.all().aggregate(Max('id'))['id__max'] + 1 if Vehicle.objects.all().exists() else 1
    while Vehicle.objects.filter(stock_number=next_vehicle_id).exists():
        next_vehicle_id += 1

    locations = Location.objects.filter(company=request.user.company)
    context = {
        'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
        'years' : range(2024, 1969, -1),
        'colors': COLORS_CONST,
        'makes_models': MAKES_MODELS,
        'form': form,
        'messages': json.loads(request.user.messages),
        'damage_types': DAMAGE_TYPE_CONST,
        'vehicles': Vehicle.objects.filter(user=request.user),
        'categories': CATEGORY_CONST,
        'stock_number': next_vehicle_id,
        'seller_types': SELLER_TYPE_CONST,
        'locations': locations,
    }
    context['form'] = form
    context['messages'] = json.loads(request.user.messages)
    request.user.messages = []
    request.user.save()
    return render(request, 'add-vehicle.html', context)

@login_required
def delete_item(request, item_id):
    if 'vehicle' in request.build_absolute_uri():
        item_to_delete = get_object_or_404(Vehicle, id=item_id)
        redirect_url = '/dashboards/vehicles/'
    else:
        item_to_delete = get_object_or_404(Part, id=item_id)
        redirect_url = '/dashboards/parts/'
    try:
        item_to_delete.delete()
        message = 'Deletion was successful.'
    except IntegrityError:
        message = 'Deletion was unsuccessful.'
    messages = json.loads(request.user.messages)
    messages.append(message)
    request.user.messages = json.dumps(messages)
    request.user.save()
    return redirect(redirect_url)
from .forms import EditPartForm, EditVehicleForm
class edit_item(LoginRequiredMixin, View):
    def get(self, request, item_id):
        if 'vehicle' in request.build_absolute_uri():
            item_to_edit = get_object_or_404(Vehicle, id=item_id)
            form = EditVehicleForm(instance=item_to_edit)
            item_edit_url = 'edit_vehicle'
            item_delete_url = 'delete_vehicle'
        else:
            item_to_edit = get_object_or_404(Part, id=item_id)
            form = EditPartForm(instance=item_to_edit)
            item_edit_url = 'edit_part'
            item_delete_url = 'delete_part'
        context = {
            'item': item_to_edit,
            'form': form,
            'item_edit_url': item_edit_url,
            'item_delete_url': item_delete_url
        }
        return render(request, 'edit-item.html', context)

    def post(self, request, item_id):
        if 'vehicle' in request.build_absolute_uri():
            item_to_edit = get_object_or_404(Vehicle, id=item_id)
            form = EditVehicleForm(request.POST, request.FILES, instance=item_to_edit)
            redirect_url = '/dashboards/vehicles/'
            if form.is_valid():
                form.save()
        else:
            item_to_edit = get_object_or_404(Part, id=item_id)
            form = EditPartForm(request.POST, request.FILES, instance=item_to_edit)
            redirect_url = '/dashboards/parts/'
            if form.is_valid() or 'images' in request.FILES:
                if form.is_valid():
                    form.save()
                else:
                    self.save_form_manually(item_to_edit, form.cleaned_data)
                self.save_images(item_to_edit, request.FILES.getlist('images'))
            else:
                print(form.errors)
        return redirect(redirect_url)
    
    def save_form_manually(self, instance, cleaned_data):
        for field, value in cleaned_data.items():
            try:
                setattr(instance, field, value)
            except Exception as e:
                print(f"Error setting field {field}: {e}")
        try:
            instance.save()
        except Exception as e:
            print(f"Error saving instance: {e}")


    def save_images(self, part, images):
        if images:
            for image in images:
                print("MAKING A PART IMAGE")
                PartImage.objects.create(part=part, image=image)
    

@login_required
def delete_vehicle(request, vehicle_id):
    vehicle_to_delete = get_object_or_404(Vehicle, id=vehicle_id)
    try:
        vehicle_to_delete.delete()
    except IntegrityError:
        add_user_message(request, 'This vehicle cannot be deleted because it is being used elsewhere')
        return redirect('single_part', vehicle_id=vehicle_id)
    add_user_message(request, 'Vehicle deleted successfully')
    return redirect('/dashboards/vehicles/')

def edit_part(request, part_id):
    part_instance = get_object_or_404(Part, id=part_id)

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
    request.user.messages = []
    request.user.save()
    return render(request, 'edit-Part.html', context)

def edit_vehicle(request, vehicle_id):
    # vehicle_instance = get_object_or_404(Vehicle, id=vehicle_id)
    # locations = Location.objects.filter(company=request.user.company)
    # # if saving edits toa part
    # if request.method == 'POST':
    #     form = VehicleForm(request.POST, request.FILES, instance=vehicle_instance)
    #     if form.is_valid():
    #         vehicle_instance = form.save(commit=False)
    #         vehicle_instance.user = request.user
    #         vehicle_instance.save()
    #         form.save()
    #         add_user_message(request, 'Vehicle updated successfully')
    #         return redirect('/dashboards/vehicles')  # Redirect to the parts list
    #     else:
    #         add_user_message(request, 'Vehicle was not updated')
    # elif is_ajax(request):
    #     location_id = request.GET.get('location_id')   
    #     lat = Location.objects.get(id=location_id).latitude
    #     lng = Location.objects.get(id=location_id).longitude
    #     location = Location.objects.filter(latitude=lat, longitude=lng)[0]
    #     vehicles = Vehicle.objects.filter(location=location)
    #     vehicles_data = serialize('List', vehicles)
    #     vehicles_data_json = json.loads(vehicles_data)
    #     return JsonResponse({'lat': lat, 'lng': lng, 'vehicles': vehicles_data_json}, safe=False)
    
    # else:
    #     form = VehicleForm(instance=vehicle_instance)
    context = {
        'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
        'years' : range(2024, 1969, -1),
        'colors': COLORS_CONST,
        'makes': ['AMC', 'Acura', 'Alfa', 'Audi', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler','Daewoo', 'Daihatsu', 'Dodge', 'Eagle', 'Fiat', 'Ford', 'GMC', 'Genesis', 'Geo', 'Honda', 'Hummer', 'Hyundai', 'IH', 'Infiniti', 'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Land Rover', 'Lexus', 'Lincoln', 'Maserati', 'Mazda', 'McLaren', 'Mercedes', 'Mercury', 'MG', 'Mini', 'Mitsubishi', 'Nissan', 'Oldsmobile', 'Pagani', 'Peugeot', 'Plymouth', 'Pontiac', 'Porsche', 'Ram', 'Renault', 'Rivian', 'Rover', 'Saab', 'Saturn', 'Scion', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Triumph', 'Volkswagen', 'Volvo'],
        'makes_models': MAKES_MODELS,
        # 'form': form,
        # 'vehicle': vehicle_instance,
        'damage_types': DAMAGE_TYPE_CONST,
        'categories': CATEGORY_CONST,
        'transmissions': TRANSMISSION_CONST,
        'seller_types': SELLER_TYPE_CONST,
        'states': STATE_CHOICES,
        # 'locations': locations,
    }
    request.user.messages = []
    request.user.save()
    return render(request, 'edit-vehicle.html', context)

class single_item(LoginRequiredMixin, View):
    def get(self, request, item_id=None, *args, **kwargs):
        item_type = None
        if 'vehicle' in request.build_absolute_uri():
            model = Vehicle
            item_edit_url = 'edit_vehicle'
            item_delete_url = 'delete_vehicle'
            item_type = 'vehicle'
        else:
            model = Part
            item_edit_url = 'edit_part'
            item_delete_url = 'delete_part'
            item_type = 'part'
        
        item = get_object_or_404(model, id=item_id)
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'messages': json.loads(request.user.messages),
            'item': item,
            'item_edit_url': item_edit_url,
            'item_delete_url': item_delete_url,
            'item_type': item_type
        }
        request.user.messages = []
        request.user.save()
        return render(request, 'single-item.html', context)

class single_vehicle(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        selected_vehicle = get_object_or_404(Vehicle, stock_number=36)
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'messages': json.loads(request.user.messages),
            'potential_profit': 0,
            'roi': 0
        }
        request.user.messages = []
        request.user.save()
        return render(request, 'single-vehicle.html', context)
    
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
        request.user.messages = []
        request.user.save()
        return render(request, 'orders.html', context)

class ebayConsent(View):
    def get(self, request):
        consent_url = "https://auth.ebay.com/oauth2/authorize?client_id=PKWhitin-Pikt-PRD-be5696659-6f69cb6d&response_type=code&redirect_uri=PK_Whiting-PKWhitin-Pikt-P-wnidgnd&scope=https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/commerce.identity.readonly https://api.ebay.com/oauth/api_scope/sell.reputation https://api.ebay.com/oauth/api_scope/sell.reputation.readonly https://api.ebay.com/oauth/api_scope/commerce.notification.subscription https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly https://api.ebay.com/oauth/api_scope/sell.stores https://api.ebay.com/oauth/api_scope/sell.stores.readonly"
        return HttpResponseRedirect(consent_url)


class yard(LoginRequiredMixin, View):
    def get(self, request, part_id=None, *args, **kwargs):
        location = request.user.location
        layout = location.layout if location.layout is not None else []
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'messages': json.loads(request.user.messages),
            'location': location,
            'location_layout': layout,
        }
        request.user.messages = []
        request.user.save()
        return render(request, 'yard.html', context)
    
    def post(self, request, part_id=None, *args, **kwargs):
        location = request.user.location
        requestType = request.headers['x-request-type']
        if requestType == 'saveYardLayout':
            incoming_markers_data = request.body
            incoming_markers_list = json.loads(incoming_markers_data) if incoming_markers_data else []
            location.layout = json.dumps(incoming_markers_list)
            location.save()

            return JsonResponse({'success': True}, safe=False)


class SalesView(LoginRequiredMixin, View):
    def get(self, request):
        start_date_str = request.GET.get('startDate')
        end_date_str = request.GET.get('endDate')

        if start_date_str and end_date_str:
            start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'))
            end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d'))
        else:
            # Default to the last 15 days
            end_date = timezone.now()
            start_date = end_date - timedelta(days=15)

        orders = Order.objects.all()
        customers = Customer.objects.filter(company=request.user.company)
        
        sold_parts = Part.objects.filter(company=request.user.company, sold=True, sold_date__isnull=False, sold_date__range=[start_date, end_date])

        sales_data = {}
        for part in sold_parts:
            date_str = part.sold_date.strftime('%b %d')
            if date_str not in sales_data:
                sales_data[date_str] = 0
            sales_data[date_str] += float(part.price)

        # Create a list of all dates in the range
        date_range = [(start_date + timedelta(days=i)).strftime('%b %d') for i in range((end_date - start_date).days + 1)]
        chart_sales = [sales_data.get(date, 0) for date in date_range]

        if is_ajax(request):
            context = {
                'chart_title': 'Sales',
                'chart_data': json.dumps(chart_sales),
                'chart_dates': json.dumps(date_range),
            }
            return JsonResponse(context)
        form = CustomerForm()
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'logo_transparent_large_black.png'),
            'years': range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'messages': json.loads(request.user.messages),
            'orders': orders,
            'customers': customers,
            'chart_title': 'Sales',
            'chart_data': json.dumps(chart_sales),
            'chart_dates': json.dumps(date_range),
            'form': form,
        }
        request.user.messages = []
        request.user.save()
        return render(request, 'sales.html', context)

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.company = request.user.company
            customer.save()
            return redirect('sales')  # Redirect to the sales view or another appropriate view
        else:
            # Handle form errors or re-render the page with errors
            return render(request, 'sales.html', {'form': form})
        
def customer_list(request):
    query = request.GET.get('q')
    if query:
        customers = Customer.objects.filter(
            Q(name__icontains=query) |
            Q(owner__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(zip_code__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        customers = Customer.objects.all()

    if is_ajax(request):
        html = render_to_string('customer-list.html', {'customers': customers})
        return JsonResponse({'html': html})

    return render(request, 'customer-search.html', {'customers': customers})


def part_search(request):
    query = request.GET.get('q')
    if query:
        # Split the query into individual terms
        query_terms = query.split()

        # Initialize the Q object for filtering parts
        parts_query = Q()
        for term in query_terms:
            term_query = (
                Q(stock_number__icontains=term) |
                Q(part_number__icontains=term) |
                Q(type__icontains=term) |
                Q(grade__icontains=term) |
                Q(interchange__icontains=term) |
                Q(vehicle__year__icontains=term) |
                Q(vehicle__make__icontains=term) |
                Q(vehicle__model__icontains=term)
            )
            # Combine the term queries with AND
            parts_query &= term_query

        parts = Part.objects.filter(parts_query)
    else:
        parts = Part.objects.all()

    if is_ajax(request):
        html = render_to_string('part-list.html', {'parts': parts})
        return JsonResponse({'html': html})

    return render(request, 'part-search.html', {'parts': parts})

from .forms import PartPreferenceForm, VehicleFilterForm
from .models import Part
from django.views.generic.detail import SingleObjectMixin
from django.forms import modelformset_factory
from .forms import PartForm
class VehiclesView(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = Vehicle.objects.filter(company=request.user.company)
        part_preference, created = PartPreference.objects.get_or_create(company=request.user.company)
        selected_parts = part_preference.get_parts_list()
        form = PartPreferenceForm(initial={'parts': selected_parts})
        filter_form = VehicleFilterForm()

        highest_stock_number = Part.get_highest_stock_number()
        parts_with_stock_numbers = []

        for i, part_type in enumerate(selected_parts, start=1):
            stock_number = highest_stock_number + i
            parts_with_stock_numbers.append({'type': part_type, 'stock_number': stock_number})

        # Create initial data for the formset
        initial_data = [
            {'type': part['type'], 'stock_number': part['stock_number']}
            for part in parts_with_stock_numbers
        ]

        PartFormSet = modelformset_factory(Part, form=PartForm, extra=len(selected_parts))
        formset = PartFormSet(queryset=Part.objects.none(), initial=initial_data)

        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'logo_transparent_large_black.png'),
            'years': range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'messages': json.loads(request.user.messages),
            'table_items': vehicles,
            'form': form,
            'filterForm': filter_form,
            'filter_form_action': reverse('filter_vehicles'),
            'item_action': 'single_vehicle',
            'filter_form_headers': list(filter_form.fields.keys()),
            'prefered_parts': parts_with_stock_numbers,
            'part_formset': formset
        }
        request.user.messages = []
        request.user.save()
        return render(request, 'vehicles.html', context)

    def post(self, request):
        part_preference, created = PartPreference.objects.get_or_create(company=request.user.company)
        form = PartPreferenceForm(request.POST, instance=part_preference)
        if form.is_valid():
            form.save()
            vehicles = Vehicle.objects.filter(company=request.user.company)
            part_preference, created = PartPreference.objects.get_or_create(company=request.user.company)
            selected_parts = part_preference.get_parts_list()
            form = PartPreferenceForm(initial={'parts': selected_parts})
            return redirect('vehicles')  # Redirect to the same page or any other page
        else:
            vehicles = Vehicle.objects.filter(company=request.user.company)
            part_preference, created = PartPreference.objects.get_or_create(company=request.user.company)
            selected_parts = part_preference.get_parts_list()
            form = PartPreferenceForm(initial={'parts': selected_parts})
            from .models import part
            highest_stock_number = Part.get_highest_stock_number()
            parts_with_stock_numbers = []

            for i, part_type in enumerate(selected_parts, start=1):
                stock_number = highest_stock_number + i
                parts_with_stock_numbers.append((part_type, stock_number))
            context = {
                'main_logo': os.path.join(settings.BASE_DIR, 'logo_transparent_large_black.png'),
                'years': range(2024, 1969, -1),
                'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
                'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
                'messages': json.loads(request.user.messages),
                'vehicles': vehicles,
                'form': form,
                'part_preference': parts_with_stock_numbers
            }
            request.user.messages = []
            request.user.save()
            return render(request, 'vehicles.html', context)
        

def inventory_addition_success(request):
    return render(request, 'add-inventory-success.html')

def create_parts(request):
    if request.method == 'POST':
        vehicle_data = {
            'vin': request.POST.get('vin'),
            'year': request.POST.get('year'),
            'make': request.POST.get('make'),
            'model': request.POST.get('model'),
            'trim': request.POST.get('trim'),
        }
        vehicle, created = Vehicle.objects.get_or_create(
            company=request.user.company,
            creator=request.user,
            vin=vehicle_data['vin'],
            year=vehicle_data['year'],
            make=vehicle_data['make'],
            model=vehicle_data['model'],
            trim=vehicle_data['trim'],
            defaults=vehicle_data
        )
        PartFormSet = modelformset_factory(Part, form=PartForm, extra=0)
        formset = PartFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.company = request.user.company
                instance.vehicle = vehicle
                
                if not Part.objects.filter(stock_number=instance.stock_number).exists():
                    instance.save()
                else:
                    highest_stock_number = Part.get_highest_stock_number()
                    instance.stock_number = highest_stock_number + 1
                    instance.save()

            add_user_message(request, 'Parts added successfully.')
        else:
            add_user_message(request, 'Failed to add parts. Please try again.')
        return redirect('vehicles')

class SavePartTypesView(LoginRequiredMixin, View):
    def post(self, request):
        selected_parts = request.POST.getlist('parts')
        # Handle the selected parts (e.g., save to the database or session)
        return JsonResponse({'status': 'success', 'selected_parts': selected_parts})


class FilterVehicles(View):
    def get(self, request, *args, **kwargs):
        vehicles = Vehicle.objects.filter(company = request.user.company)
        # filter only searches for single characters, it needs to search for characters and strings
        if request.GET.get('vin'):
            vehicles = vehicles.filter(vin__icontains=request.GET.get('vin'))
        if request.GET.get('make'):
            vehicles = vehicles.filter(make__icontains=request.GET.get('make'))
        if request.GET.get('model'):
            vehicles = vehicles.filter(model__icontains=request.GET.get('model'))
        if request.GET.get('year'):
            vehicles = vehicles.filter(year__icontains=request.GET.get('year'))
        if request.GET.get('trim'):
            vehicles = vehicles.filter(trim__icontains=request.GET.get('trim'))
        if request.GET.get('location'):

            vehicles = vehicles.filter(location__icontains=request.GET.get('location'))
        context = {
            'table_items': vehicles, 
            'filter_form_headers': ['vin', 'year', 'make', 'model', 'trim', 'location'], 
            'filter_form_action': 'filter_vehicles',
            'table_items': vehicles,
            'item_action': 'single_vehicle',
        }
        html = render_to_string('filtered-table.html', context)
        return JsonResponse({'html': html})

class FilterParts(View):
    def get(self, request, *args, **kwargs):
        parts = Part.objects.filter(company=request.user.company, sold=False)
        # filter only searches for single characters, it needs to search for characters and strings
        if request.GET.get('type'):
            parts = parts.filter(type__icontains=request.GET.get('type'))
        if request.GET.get('stock_number'):
            parts = parts.filter(stock_number__icontains=request.GET.get('stock_number'))
        if request.GET.get('location'):
            parts = parts.filter(location__icontains=request.GET.get('location'))
        if request.GET.get('grade'):
            parts = parts.filter(grade__icontains=request.GET.get('grade'))
        if request.GET.get('ebay_listed'):
            parts = parts.filter(ebay_listed=bool(request.GET.get('ebay_listed')))
        if request.GET.get('marketplace_listed'):
            parts = parts.filter(marketplace_listed=bool(request.GET.get('marketplace_listed')))

        context = {
            'table_items': parts,
            'filter_form_headers': ['stock_number', 'type', 'location', 'grade', 'ebay_listed', 'marketplace_listed'],
            'filter_form_action': 'filter_parts',
            'table_items': parts,
            'item_action': 'single_part',
        }
        html = render_to_string('filtered-table.html', context)
        return JsonResponse({'html': html})