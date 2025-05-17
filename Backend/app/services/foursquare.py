# app/services/foursquare.py
import requests
import os

def get_hotels(city: str):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {"Authorization": os.getenv("FOURSQUARE_API_KEY")}
    params = {
        "query": "hotel",
        "near": city,
        "limit": 5,
        "fields": "name,location,website"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "name": place.get('name', ''),
                "address": place.get('location', {}).get('formatted_address', ''),
                "website": place.get('website', '')
            } 
            for place in data.get('results', [])
        ]
    except requests.exceptions.RequestException as e:
        print(f"Foursquare API error: {e}")
        return []