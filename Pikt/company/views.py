from django.shortcuts import render, redirect
from django.views import View
from Authentication.models import User
from .models import Location, ShippingAddress, BillingAddress
from .forms import UserForm
import json
from django.templatetags.static import static
from Authentication.forms import RegisterForm

avatar_url = static('icons/avatar.webp')

def add_user_message(request, message):
    messages = json.loads(request.user.messages)
    messages.append(message)
    request.user.messages = json.dumps(messages)
    request.user.save()

# Create your views here.
class rootView(View):
    
    def get(self, request):
        if request.user.role != 'Admin':
            return redirect(request.META.get('HTTP_REFERER', 'vehicles'))
        form = RegisterForm()
        del form.fields['company']
        company = request.user.company
        users = User.objects.filter(company=company).exclude(id=request.user.id)
        return render(request, 'company.html', {'form': form, 'users': users})
    def post(self, request):
        if request.user.role != 'Admin':
            return redirect(request.META.get('HTTP_REFERER', 'vehicles'))
        form = RegisterForm(request.POST)
        del form.fields['company']
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            role = request.POST.get('role')
            if role == 'Admin':
                role = 'Manager'
            elif role == 'User':
                role = 'Employee'
            company = request.user.company
            icon = '../static/images/default-avatar.webp'
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'A user with this email already exists')
                return render(request, 'company.html', {'form': form})
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'A user with this username already exists')
                return render(request, 'company.html', {'form': form})
            
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name, icon=icon, role=role, company=company)
            messages = json.loads(request.user.messages)
            messages.append('User added successfully!')
            request.user.messages = json.dumps(messages)
            request.user.save()
            return redirect('/dashboards/vehicles/', {'form': form})
        return render(request, 'company.html', {'form': form})

    def render_form(self, request, form):
        company = request.user.company
        users = User.objects.filter(company=company).exclude(id=request.user.id)
        locations = Location.objects.filter(company=company)
        context = {
            'users': users,
            'company': company,
            'locations': locations,
            'form': form
        }
        return render(request, 'company.html', context)
        