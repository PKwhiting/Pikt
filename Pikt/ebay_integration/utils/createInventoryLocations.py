import requests
import json

def create_inventory_locations(user, merchantLocationKey, address, geoCoordinates, locationAdditionalInformation, locationInstructions, locationTypes, locationWebUrl, merchantLocationStatus, name, operatingHours, phone, specialHours):
    url = f"https://api.ebay.com/sell/inventory/v1/location/{merchantLocationKey}"

    headers = {
        'Authorization': f'Bearer {user.ebay_user_token}',
        'Content-Type': 'application/json',
    }

    payload = {
        "location": {
            "address": address,
            "geoCoordinates": geoCoordinates
        },
        "locationAdditionalInformation": locationAdditionalInformation,
        "locationInstructions": locationInstructions,
        "locationTypes": locationTypes,
        "locationWebUrl": locationWebUrl,
        "merchantLocationStatus": merchantLocationStatus,
        "name": name,
        "operatingHours": operatingHours,
        "phone": phone,
        "specialHours": specialHours
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return response