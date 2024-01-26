from django.shortcuts import render, redirect
from .utils.bulkCreateOrReplaceInventoryItem import create_inventory_item
from .utils.bulkUpdatePriceQuantity import update_price_quantity
from .utils.getInventoryLocation import get_inventory_location
from dashboards.models import part
from django.contrib.auth.decorators import login_required
import json

def add_user_message(user, message):
    messages = json.loads(user.messages)
    messages.append(message)
    user.messages = json.dumps(messages)
    user.save()

# Create your views here.
@login_required
def create_ebay_listing(request, part_id):
    user = request.user
    if user.handle_tokens():
        locations = get_inventory_location(user)
        print(locations)
        # if 'locations' in locations and len(locations['locations']) > 0:
        #     location_id = locations['locations'][0]['location']['locationId']
        # else:
        #     add_user_message(user, "No locations found")
        #     return redirect('/dashboards/')

        # print("IN THE RIGHT PLACE")
        # selected_part = part.objects.get(id=part_id)
        # response_1 = create_inventory_item(user, selected_part)
        # print(response_1.json())
        

        # print(response_2.json())

        # response_2 = update_price_quantity(user, selected_part, location_id)
        # print(response_2.json())

        # if response_1.status_code == 200:
        #     add_user_message(user, "Ebay listing created")
    return redirect('/dashboards/')
    
        


