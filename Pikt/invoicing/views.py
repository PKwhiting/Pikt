from django.shortcuts import render
from .models import Invoice
from company.models import Company
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
import json
from  dashboards.models import Customer
import pdfkit
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
import re
from dashboards.models import Part

def add_user_message(request, message):
    messages = json.loads(request.user.messages)
    messages.append(message)
    request.user.messages = json.dumps(messages)
    request.user.save()

def extract_first_number(description):
    # Use regular expressions to find the first number in the description
    match = re.search(r'\b\d+\b', description)
    if match:
        return int(match.group())
    else:
        return None

# Create your views here.
def generate_quote(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    # create an invoice object
    invoice = Invoice.objects.create(
        company=request.user.company,
        user=request.user,
        destination=customer,
        status='Draft',
    )
    invoice.save()

    context = {
            'main_logo': os.path.join(settings.BASE_DIR, 'logo_transparent_large_black.png'),
            'years' : range(2024, 1969, -1),
            'colors': ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Brown', 'Green', 'Yellow', 'Gold', 'Orange', 'Purple'],
            'makes': ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani', 'Peugeot', 'Porsche', 'Ram', 'Renault', 'Rolls Royce', 'Saab', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo'],
            'messages': json.loads(request.user.messages),
            'customer': customer,
            'invoice': invoice,
        }
    return render(request, 'invoice.html', context)

def send_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    data_str = request.body.decode('utf-8')
    data_json = json.loads(data_str)

    due_date = data_json['dueDate']
    invoice.due_date = due_date

    stock_numbers = []
    for obj in data_json['parts']:
        stock_number = extract_first_number(obj['description'])
        if stock_number is not None:
            stock_numbers.append(stock_number)

    parts = []
    for stock_number in stock_numbers:
        part = Part.objects.get(stock_number=stock_number, company=request.user.company)
        parts.append(part)
    
    parts_total = sum([part.price for part in parts])
    invoice.total = parts_total
    
    context = {
        'parts': parts,
        'invoice': invoice,
        'customer': invoice.destination,
        'user': request.user,
        'parts_total': parts_total
    }


    html_string = render_to_string('invoice-template.html', context)
    invoice.html = html_string
    invoice.save()
    pdf_file = pdfkit.from_string(html_string, False)


    email = EmailMessage(
        subject=f'Invoice from {request.user.company.name}',
        body='Please find the attached invoice.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[invoice.destination.email],  
    )
    email.attach('invoice.pdf', pdf_file, 'application/pdf')
    email.send()

    add_user_message(request, 'Invoice sent succesfully!')

    return JsonResponse({'status': 'success'})