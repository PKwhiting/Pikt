from django.shortcuts import render
from django.views import View
from Authentication.models import User

# Create your views here.
class rootView(View):
    def get(self, request):
        company = request.user.company
        users = User.objects.filter(company=company).exclude(id=request.user.id)
        locations = company.location_set.all()
        context = {
            'users': users,
            'company': company,
            'locations': locations,
        }
        return render(request, 'company.html', context)