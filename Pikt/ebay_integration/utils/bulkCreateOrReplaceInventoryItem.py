import requests
import json
import base64
import os
from django.conf import settings
import os
from django.db import models


def create_inventory_item(user, part):
    url = "https://api.sandbox.ebay.com/sell/inventory/v1/bulk_create_or_replace_inventory_item"

    headers = {
        'Authorization': f'Bearer {user.ebay_user_token}',
        'Content-Language': 'en-US',
        "Content-Type": 'application/json'
    }
    image_urls = get_image_urls(part)
    payload = {
        "requests": [
            {
                "availability": {
                    "shipToLocationAvailability": {
                        "quantity": "1"
                    }
                },
                "condition": "USED_EXCELLENT",
                "conditionDescription": f'{part.notes}',
                "locale": "en_US",
                "sku": f'{part.sku}',
            }
        ]

    }


    response = requests.post(url, headers=headers, json=payload)

    return response

def get_image_urls(part_instance):
    image_urls = []
    for field in part_instance._meta.fields:
        if isinstance(field, models.ImageField):
            image = getattr(part_instance, field.name)
            if image and hasattr(image, 'url'):
                # Ensure we have a complete url (including domain name)
                if settings.DEBUG:
                    image_url = 'http://localhost:8000' + image.url
                else:
                    image_url = 'https://your-production-domain.com' + image.url
                image_urls.append(image_url)
    return image_urls

