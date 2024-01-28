from django.shortcuts import render
from django.views import View
from Authentication.models import User
from .models import Location

# Create your views here.
class rootView(View):
    def get(self, request):
        company = request.user.company
        users = User.objects.filter(company=company).exclude(id=request.user.id)
        locations = Location.objects.filter(company=company)
        context = {
            'users': users,
            'company': company,
            'locations': locations,
        }
        return render(request, 'company.html', context)