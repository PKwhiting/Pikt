import requests
import json
import base64
import os
from django.conf import settings
import os
from django.db import models


def get_inventory_location(user):
    url = "https://api.ebay.com/sell/inventory/v1/location"

    headers = {
        'Authorization': f'Bearer {user.ebay_user_token}',
    }

    response = requests.get(url, headers=headers)
    print("HERE IS THE RESPONSE")
    print(response)

    return response.json()
