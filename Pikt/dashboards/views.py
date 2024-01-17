from django.shortcuts import render, redirect
from django.views import View
from .models import part
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PartForm
from django.core.paginator import Paginator
import json
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required


context = {
    'main_logo': os.path.join(settings.BASE_DIR, 'assets', 'logo_transparent_large_black.png'),
    'years' : range(2024, 1969, -1),
    'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
    'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo']
}

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
        context['messages'] = json.loads(request.user.messages)
        return render(request, 'root.html', context)
 
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
        form = PartForm(request.POST, request.FILES)
        if form.is_valid():
            part = form.save(commit=False)
            part.user = request.user
            images = request.FILES.getlist('images')
            for i in range(1, min(11, len(images) + 1)):
                image_field = f'part_image_{i}'
                setattr(part, image_field, images[i-1])
            form.save()
            messages = json.loads(request.user.messages)
            messages.append('Part added successfully')
            request.user.messages = json.dumps(messages)
            request.user.save()
            return redirect('/dashboards/parts')  # Redirect to a page showing all parts
    else:
        form = PartForm()
    context['form'] = form
    return render(request, 'add-part.html', context)