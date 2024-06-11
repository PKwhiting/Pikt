from django.shortcuts import render, redirect
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
        parts = Part.objects.filter(user=request.user).order_by('-created_at')[:3]
        # get the price of all parts from the user that have a status of 'sold'
        sold_parts = Part.objects.filter(user=request.user, status='Sold')
        total_revenue = round(sold_parts.aggregate(Sum('price'))['price__sum'], 2) if sold_parts.aggregate(Sum('price'))['price__sum'] is not None else '0.00'
        shipped_parts = Part.objects.filter(user=request.user, status='Shipped')
        unsold_parts = Part.objects.filter(user=request.user, status__in=['Pending', 'Listed'])
        average_price = unsold_parts.aggregate(Avg('price'))['price__avg'] if unsold_parts.aggregate(Avg('price'))['price__avg'] is not None else '0.00'
        last_15_days = []
        for i in range(15, -1, -1):
            last_15_days.append((datetime.now() - timedelta(days=i)).strftime('%b-%d'))

        start_date = datetime.now() - timedelta(days=15)

        # Get the number of vehicles created each day for the last 15 days
        vehicles_created_each_day = Vehicle.objects.filter(
            location=request.user.location,
            created_at__gte=start_date
        ).annotate(
            date=TruncDate('created_at')
        ).values(
            'date'
        ).annotate(
            total_created=Count('id')
        ).order_by('date')

        # Convert QuerySet to a format suitable for the graph
        vehicles_created_each_day_data = []
        for i in range(15, -1, -1):
            date = (datetime.now() - timedelta(days=i)).date()
            # Try to find a match in our query results
            match = next((item for item in vehicles_created_each_day if item['date'] == date), None)
            total_created = match['total_created'] if match else 0
            vehicles_created_each_day_data.append(
                total_created,
            )

        current_month = datetime.now().month
        current_year = datetime.now().year


        vehicles_bought_this_month = Vehicle.objects.filter(
            user=request.user,
            created_at__month=current_month,
            created_at__year=current_year
        ).count()


        recent_vehicles = Vehicle.objects.filter(user=request.user).order_by('-created_at')[:5]

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
            'chartLabels': json.dumps(last_15_days),
            'chartData': vehicles_created_each_day_data,
            'mtd_purchases': vehicles_bought_this_month,
            'recent_vehicles': recent_vehicles,
        }

        request.user.messages = []
        request.user.save()
        return render(request, 'dashboard.html', context)
 
class defaultDashboardView(LoginRequiredMixin,View):
    def get(self, request):
        parts = Part.objects.filter(user=request.user) if request.user.is_authenticated else []
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
            'years': range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'parts': parts,
            'messages': json.loads(request.user.messages),
            'makes_models': MAKES_MODELS,
            'part_types': PARTS_CONST,
        }
        if is_ajax(request):
            year_start = request.GET.get('year_start')
            year_end = request.GET.get('year_end')
            vehicle_make = request.GET.get('vehicle_make')
            vehicle_model = request.GET.get('vehicle_model')
            part_type = request.GET.get('part_type')
            part_grade = request.GET.get('grade')
            parts = Part.objects.filter(user=request.user)
            if year_start:
                parts = parts.filter(vehicle_year__gte=year_start)
            if year_end:
                parts = parts.filter(vehicle_year__lte=year_end)
            if vehicle_model:
                parts = parts.filter(vehicle_model__icontains=vehicle_model)
            if vehicle_make:
                parts = parts.filter(vehicle_make__icontains=vehicle_make)
            if part_type:
                parts = parts.filter(type__iexact=part_type)
            if part_grade:
                parts = parts.filter(grade__iexact=part_grade)
            context['parts'] = parts
            return HttpResponse(render_to_string('parts-table.html', context))
        if context['parts'].count() > 0:
            parts_list = Part.objects.filter(user=request.user).order_by('id')
            paginator = Paginator(parts_list, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['parts'] = page_obj
        request.user.messages = []
        request.user.save()
        return render(request, 'parts.html', context)

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
    return redirect('/dashboards/vehicles/')

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
            'potential_profit': (selected_Part.price or Decimal('0.01')) - (selected_Part.cost or Decimal('0.01')),
            'roi': round(((selected_Part.price or Decimal('0.01')) - (selected_Part.cost or Decimal('0.01'))) / (selected_Part.cost or Decimal('0.01')) * 100, 2)   
        }
        request.user.messages = []
        request.user.save()
        return render(request, 'single-Part.html', context)

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


import pandas as pd
class parts(View):
    def post(self, request):
        if 'inventory' in request.FILES:
            file = request.FILES['inventory']
            try:
                # Read the file into a pandas DataFrame
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file, engine='openpyxl')
                elif file.name.endswith('.xls'):
                    df = pd.read_excel(file, engine='xlrd')
                else:
                    add_user_message(request, 'Invalid file format. Please upload a CSV or Excel file.')
                    return redirect('upload_inventory')
                
                df = df.iloc[:, :5]

                # Convert DataFrame to a list of dictionaries
                data = df.to_dict(orient='records')

                for row in data:
                    new_part, created = Part.objects.get_or_create(
                        stock_number=row['STOCK_NUMBER'],
                        defaults={
                            'user': request.user,
                            'hollander_interchange': row['INTERCHANGE'],
                            'type': row['NAME'],
                            'category': row['CATEGORY'],
                            'vehicle_vin': row['VIN'],
                        }
                    )
                    if created:
                        print(f"Created new part: {new_part}")
                    else:
                        print(f"Part already exists: {new_part}")

                # Save the DataFrame to the session to display it in the template
                request.session['table_data'] = data
                add_user_message(request, 'Inventory uploaded successfully.')

            except Exception as e:
                add_user_message(request, f'Error: {e}')
                return redirect('parts')
        return redirect('parts')

    def get(self, request):
        # total_parts_count = Part.objects.filter(user=request.user).count()
        # max_cores = core.objects.filter(interchange=OuterRef('hollander_interchange')).order_by().values('interchange').annotate(max_price=Max('price'))
        # parts_with_max_core = Part.objects.filter(user=request.user).annotate(max_core_price=Subquery(max_cores.values('max_price')))
        # total_max_core_price = parts_with_max_core.aggregate(total=Sum('max_core_price'))['total']
        # total_max_core_price = Decimal(total_max_core_price).quantize(Decimal('0.00'))
        # del request.session['table_data']
        table_data = request.session.get('table_data', '')
        parts = Part.objects.filter(user=request.user).order_by('id')
        context = {
            'table_data': table_data,
            'parts': parts,
            'messages': json.loads(request.user.messages),
        }
        return render(request, 'parts.html', context)
    
# define the sales view and render sales.html
class sales(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all()
        customers = Customer.objects.filter(company=request.user.company)
        context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'messages': json.loads(request.user.messages),
            'orders': orders,
            'customers': customers,
        }
        request.user.messages = []
        request.user.save()
        return render(request, 'sales.html', context)

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
        print(request)
        html = render_to_string('customer-list.html', {'customers': customers})
        return JsonResponse({'html': html})

    return render(request, 'customer-search.html', {'customers': customers})

def generate_quote(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'messages': json.loads(request.user.messages),
            'orders': orders,
            'customer': customer,
        }
    return render(request, 'invoice.html', context)


def part_search(request):
    query = request.GET.get('q')
    if query:
        parts = Part.objects.filter(
            Q(vehicle_year__icontains=query) |
            Q(vehicle_make__icontains=query) |
            Q(vehicle_model__icontains=query) |
            Q(type__icontains=query) |
            Q(grade__icontains=query) |
            Q(hollander_interchange__icontains=query)
        )
    else:
        parts = Part.objects.all()

    if is_ajax(request):
        html = render_to_string('part-list.html', {'parts': parts})
        return JsonResponse({'html': html})

    return render(request, 'part-search.html', {'parts': parts})

def send_invoice(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    print(customer)
    context = {
        'user': request.user,
        'customer': customer,
    }
    html_string = render_to_string('invoice_email.html', context)
    pdf_file = pdfkit.from_string(html_string, False)

    email = EmailMessage(
        subject='Your Invoice',
        body='Please find the attached invoice.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[customer.email],
    )
    email.attach('invoice.pdf', pdf_file, 'application/pdf')
    email.send()

    return JsonResponse({'message': 'Invoice sent successfully!'})

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
        filterForm = VehicleFilterForm()

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
            'vehicles': vehicles,
            'form': form,
            'filterForm': filterForm,
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
        print(formset)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.company = request.user.company
                instance.vehicle = vehicle
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
        if request.GET.get('stock_number'):
            vehicles = vehicles.filter(vin__icontains=request.GET.get('vin'))
        if request.GET.get('make'):
            vehicles = vehicles.filter(make__icontains=request.GET.get('make'))
        if request.GET.get('model'):
            vehicles = vehicles.filter(model__icontains=request.GET.get('model'))
        if request.GET.get('year'):
            vehicles = vehicles.filter(year__icontains=request.GET.get('year'))
        html = render_to_string('vehicle-list.html', {'vehicles': vehicles})
        return JsonResponse({'html': html})
