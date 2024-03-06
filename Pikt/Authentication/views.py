from django.shortcuts import render
from .models import User
from django.contrib.auth import login
import os
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from dotenv import load_dotenv
from .models import templateImage
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import json
from .forms import FunnelSubmissionForm

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
            return redirect('/dashboards/')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboards/')  # replace 'home' with the name of the view you want to redirect to after login
        else:
            # Invalid login
            return render(request, 'login.html', {'error': 'Invalid username or password'})

class registerView(View):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        username = request.POST['Username']
        password = request.POST['Password']
        email = request.POST['Email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        icon = '../static/images/default-avatar.webp'
        if User.objects.filter(username=username).exists():
            # If the user already exists, return an error message
            return render(request, 'register.html', {'error': 'A user with this username already exists'})
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name, icon=icon)
        login(request, user)
        messages = json.loads(request.user.messages)
        messages.append('Welcome to Pikt! Get started by adding your first part!')
        messages.append('After you add your first part, it will appear below in the parts table.')
        messages.append('Once you list your part, our software works with ebay to get it listed under our ebay, mercari, and offerup accounts.')
        messages.append('Within 24 hours a link will appear in the part row that will take you to that parts ebay listing. We are working on making the mercari and offerup link available.')
        messages.append('Once a part is sold we will send you a shipping label and send you payment for the part.')
        messages.append('If you have any questions, please contact us at pwhiting@simpli-cars.com')
        request.user.messages = json.dumps(messages)
        request.user.save()
        return redirect('/dashboards/')

class passwordResetView(View):
    def get(self, request):
        return render(request, 'password-reset.html')

    def post(self, request):
        return render(request, 'password-reset.html')
 
class accountView(View):
    def get(self, request):
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