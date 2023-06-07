import requests
import os
from dotenv import load_dotenv

load_dotenv()

TEQUILLA_API_KEY = os.getenv('TEQUILLA_API_KEY')
TEQUILLA_ENDPOINT = os.getenv('TEQUILLA_ENDPOINT')


class FlightSearch:
    # his class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.flight_detail = {}
        self.headers = {
            "apikey": TEQUILLA_API_KEY,
        }

    def get_iata_code(self, city_name: str) -> str:
        parameters = {
            "term": city_name,
        }
        response = requests.get(url=f"{TEQUILLA_ENDPOINT}/locations/query", headers=self.headers, params=parameters)
        data = response.json()
        city_code = data["locations"][0]["code"]
        return city_code

    def search_flight(self, date_from: str, date_to: str, fly_from: str, fly_to: str):
        body_data = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": str(date_from),
            "date_to": str(date_to),
            "curr": "USD"
        }
        try:
            response = requests.get(url=f"{TEQUILLA_ENDPOINT}/v2/search", headers=self.headers, params=body_data)
            response.raise_for_status()
            self.flight_detail = response.json()
        except:
            self.flight_detail = None
        else:
            return self.flight_detail
