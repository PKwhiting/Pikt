from django.shortcuts import render, redirect
from django.views import View
from Authentication.models import User
from .models import Location, ShippingAddress, BillingAddress
from .forms import UserForm
import json
from django.templatetags.static import static
from Authentication.forms import RegisterForm
from .forms import CompanyForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.html import strip_tags
import os

avatar_url = static('icons/avatar.webp')

def add_user_message(request, message):
    messages = json.loads(request.user.messages)
    messages.append(message)
    request.user.messages = json.dumps(messages)
    request.user.save()

# Create your views here.
def update_company(request):
    if request.method == 'POST':
        company_form = CompanyForm(request.POST, request.FILES, instance=request.user.company)
        if company_form.is_valid():
            company_form.save()
            return redirect('dashboard')
    else:
        company_form = CompanyForm(instance=request.user.company)
    return render(request, 'company.html', {'company_form': company_form})

class rootView(View):
    def get(self, request):
        company = request.user.company
        company_form = CompanyForm(instance=company)
        if request.user.role != 'Admin':
            return redirect(request.META.get('HTTP_REFERER', 'vehicles'))
        register_user_form = RegisterForm()
        del register_user_form.fields['company']
        company = request.user.company
        users = User.objects.filter(company=company).exclude(id=request.user.id)
        context = {
            'years' : range(2024, 1969, -1),
            'form': register_user_form,
            'messages': json.loads(request.user.messages),
            'users': users,
            'company_form': company_form
        }
        return render(request, 'company.html', context)
    
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

            subject = 'Pikt Account Details'
            html_message = f'''
                <p>Hello {first_name},</p>
                <p>Your account has been created.</p>
                <p>Username: <strong>{username}</strong><br>
                Email: <strong>{email}</strong></p>
                <p>Click here to set your password: <a href="https://piktparts.com/accounts/password_reset/">Set Password</a></p>
                <p>Thank you!</p>
                <p>Team Pikt</p>
            '''
            plain_message = strip_tags(html_message)
            from_email = os.getenv('GMAIL_EMAIL')
            to_email = [email]

            send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
            messages = json.loads(request.user.messages)
            messages.append('User added successfully!')
            request.user.messages = json.dumps(messages)
            request.user.save()
            return redirect('/company/', {'form': form})
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
        