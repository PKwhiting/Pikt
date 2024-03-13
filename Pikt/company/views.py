from django.shortcuts import render, redirect
from django.views import View
from Authentication.models import User
from .models import Location, ShippingAddress, BillingAddress
from .forms import UserForm
import json
from django.templatetags.static import static

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
        else:
            company = request.user.company
            shippingAddress = ShippingAddress.objects.filter(company=company)
            users = User.objects.filter(company=company).exclude(id=request.user.id)
            form = UserForm()
            context = {
                'users': users,
                'company': company,
                'form': form,
                'address': shippingAddress[0]
            }
            return render(request, 'company.html', context)
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.company = request.user.company
            user.location = request.user.location
            user.icon = avatar_url
            user.save()
            company = request.user.company
            users = User.objects.filter(company=company).exclude(id=request.user.id)
            form = UserForm()
            add_user_message(request, f'User {user.username} added')
            context = {
                'users': users,
                'form': form,
                'messages': json.loads(request.user.messages)
            }
            request.user.messages = []
            request.user.save()
            return render(request, 'company.html', context)
        else:
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
        