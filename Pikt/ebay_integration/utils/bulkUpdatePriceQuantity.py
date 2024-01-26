import requests
import json
import base64
import os
from django.conf import settings
import os
from django.db import models


def update_price_quantity(user, part):
    url = "https://api.sandbox.ebay.com/sell/inventory/v1/bulk_update_price_quantity"

    headers = {
        'Authorization': f'Bearer {user.ebay_user_token}',
        'Content-Language': 'en-US',
        "Content-Type": 'application/json'
    }

    payload = {
        "requests": [
            {
                "offers": [
                    {
                        "price": {
                            "currency": "USD",
                            "value": f'{part.price}'
                        }
                    }
                ],
                "sku": f'{part.sku}'
            }
        ]


    }
    print(payload)

    response = requests.post(url, headers=headers, json=payload)

    return response
