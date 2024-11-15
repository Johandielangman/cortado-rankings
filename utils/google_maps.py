from requests.exceptions import RequestException
from typing import Dict
import requests
import re


class GoogleMapsConverter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.place_api_url = "https://maps.googleapis.com/maps/api/place/details/json"
        self.short_url_pattern = r'^https://maps\.app\.goo\.gl/[A-Za-z0-9_-]+$'
        self.place_id_patterns = [
            r'!1s(0x[0-9a-fA-F]+:0x[0-9a-fA-F]+)',
            r'0x[0-9a-fA-F]+:0x[0-9a-fA-F]+'
        ]

    def validate_short_url(self, url: str) -> bool:
        if not re.match(self.short_url_pattern, url):
            raise ValueError("Invalid Google Maps short URL format")
        return True

    def resolve_short_url(self, short_url: str) -> str:
        try:
            response = requests.get(short_url, allow_redirects=True)
            response.raise_for_status()
            return response.url
        except RequestException as e:
            raise Exception(f"Error resolving short URL: {str(e)}")

    def extract_place_id(self, full_url: str) -> str:
        for pattern in self.place_id_patterns:
            match = re.search(pattern, full_url)
            if match:
                return match.group(1) if '!1s' in pattern else match.group(0)
        raise ValueError("Could not find place ID in URL")

    def get_place_details(self, place_id: str) -> Dict:
        params = {
            'key': self.api_key,
            'ftid': place_id
        }
        try:
            response = requests.get(self.place_api_url, params=params)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise Exception(f"Error fetching place details: {str(e)}")

    def process_url(self, short_url: str) -> Dict:
        try:
            self.validate_short_url(short_url)
            full_url = self.resolve_short_url(short_url)
            place_id = self.extract_place_id(full_url)

            return self.get_place_details(place_id)
        except Exception as e:
            return {"error": str(e)}
