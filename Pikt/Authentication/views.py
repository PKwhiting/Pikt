from django.shortcuts import render
from .models import User
from django.contrib.auth import login
import os
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from dotenv import load_dotenv
from .models import templateImage
from company.models import Company, Location
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import json
from .forms import FunnelSubmissionForm, RegisterForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django import forms
from django.contrib.auth.views import PasswordResetDoneView

from dashboards.models import PartPreference


context = {
    'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
    'years' : range(2024, 1969, -1),
    'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
    'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo']
}

class MyView(View):
    def get(self, request):
        load_dotenv()
        context = {
            'APPLICATION_TOKEN': os.getenv('APPLICATION_TOKEN'),
            'USER_TOKEN': os.getenv('USER_TOKEN')
        }
        return render(request, 'index.html', context)
# Create your views here.

class homeView(View):
    def get(self, request):
        form = FunnelSubmissionForm()
        transparent_logo_large_white  = os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_white.png')
        context = {
            'form': form,
            'transparent_logo_large_white': transparent_logo_large_white
        }
        return render(request, 'home.html', context)

    def post(self, request):
        transparent_logo_large_white  = os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_white.png')
        form = FunnelSubmissionForm(request.POST)
        
        if form.is_valid():
            if form.cleaned_data['otherInput']:
                instance = form.save(commit=False)
                instance.message = form.cleaned_data['otherInput']
                instance.save()
            else:
                form.save()
            context = {
                'transparent_logo_large_white': transparent_logo_large_white
            }
            return render(request, 'funnel-success.html', context)  # replace 'success_url' with the name of the URL you want to redirect to after successful form submission
        else:
            transparent_logo_large_white  = os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_white.png')
            context = {
                'form': form,
                'transparent_logo_large_white': transparent_logo_large_white
            }
            return render(request, 'home.html', context)

class loginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/dashboards/vehicles/')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboards/vehicles/')  # replace 'home' with the name of the view you want to redirect to after login
        else:
            # Invalid login
            return render(request, 'login.html', {'error': 'Invalid username or password'})

class registerView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            company = form.cleaned_data['company']
            icon = '../static/images/default-avatar.webp'
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'A user with this email already exists')
                return render(request, 'register.html', {'form': form})
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'A user with this username already exists')
                return render(request, 'register.html', {'form': form})
            if Company.objects.filter(name=company).exists():
                form.add_error('company', 'A company with this name already exists')
                return render(request, 'register.html', {'form': form})
            company = Company.objects.create(name=company)
            PartPreference.objects.create(company=company, parts="A/C Compressor,Alternator,Axle Assy Fr (4WD w. Housing),Axle Assy Rear (w. Housing),Battery,Brake/Clutch Pedal,Brake Booster,Brake Rotor/Drum, Rear,Bumper Assy (Front) includes cover,Bumper Assy (Rear) includes cover,Caliper,Clutch Master Cylinder,Control Arm, Front Lower,Control Arm, Front Upper,Control Arm, Rear Lower,Control Arm, Rear Upper,Door Back (door above rear bumper),Door Front,Engine,Engine Computer,Engine Wiring Harness,Fender,Front Axle Assembly (4WD w Housing),Front Bumper Assembly (includes cover),Master Cylinder,Transmission,Windshield")
            company.save
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name, icon=icon, company=company)
            user.role = "Admin"
            user.save()
            login(request, user)
            messages = json.loads(request.user.messages)
            messages.append('Welcome to Pikt!')
            request.user.messages = json.dumps(messages)
            request.user.save()
            return redirect('/dashboards/vehicles/')
        return render(request, 'register.html', {'form': form})

    
from dashboards.models import Customer
from invoicing.models import Invoice
from ebay.models import EbayPolicy, EbayCredential
from ebay.forms import EbayPolicyForm, EbayMIPCredentialsForm
class accountView(View):
    def get(self, request):
        payment_ebay_policy_form = EbayPolicyForm(initial={'company': request.user.company, 'policy_type': 'Payment'})
        payment_ebay_policy_form.fields['company'].widget = forms.HiddenInput()
        return_ebay_policy_form = EbayPolicyForm(initial={'company': request.user.company, 'policy_type': 'Return'})
        return_ebay_policy_form.fields['company'].widget = forms.HiddenInput()
        shipping_ebay_policy_form = EbayPolicyForm(initial={'company': request.user.company, 'policy_type': 'Shipping'})
        shipping_ebay_policy_form.fields['company'].widget = forms.HiddenInput()

        ebay_mip_credentials_form = EbayMIPCredentialsForm()
        

        ebay_credentials_exist = False
        if request.user.company.ebay_credentials:
            ebay_credentials_exist = True

        context = {
            'customer_count': Customer.objects.all().count(),
            'invoices_total': "{:.2f}".format(sum(invoice.total for invoice in Invoice.objects.filter(company=request.user.company) if invoice.total is not None)),
            'invoices': Invoice.objects.filter(company=request.user.company),
            'payment_ebay_policy_form': payment_ebay_policy_form,
            'return_ebay_policy_form': return_ebay_policy_form,
            'shipping_ebay_policy_form': shipping_ebay_policy_form,
            'ebay_mip_credentials_form': ebay_mip_credentials_form,
            'ebay_credentials_exist': ebay_credentials_exist,
            'messages': json.loads(request.user.messages),
        }
        return render(request, 'account.html', context)
    
    def post(self, request):
        first_name = request.POST.get('First-name')
        last_name = request.POST.get('Last-name')
        email = request.POST.get('Email-Address')
        phone_number = request.POST.get('Phone')

        user = request.user
        if first_name != '':
            user.first_name = first_name
        if last_name != '':
            user.last_name = last_name
        if email != '':
            user.email = email
        if phone_number != '':
            user.phone_number = phone_number
        user.save()

        # messages.success(request, 'Your account has been updated!')
        return redirect('account')
    
class uploadAvatarView(View):
    def post(self, request):
        if 'icon' in request.FILES:
            request.user.icon = request.FILES['icon']
            request.user.save()
            # messages.success(request, 'Avatar updated successfully')
        return redirect('account')