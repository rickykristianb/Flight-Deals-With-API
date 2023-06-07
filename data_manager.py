import requests
import flight_search
from dotenv import load_dotenv
import os

load_dotenv()

GET_SHETTY_ENDPOINT = os.getenv('GET_SHETTY_ENDPOINT')
EDIT_SHETTY_ENDPOINT = os.getenv('EDIT_SHETTY_ENDPOINT')


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_sheets_data(self):
        response = requests.get(url=GET_SHETTY_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def set_iatacode(self):
        for detail in self.destination_data:
            if detail["iataCode"] == "":
                object_id = detail["id"]
                city = detail["city"]
                self.update_to_sheet(id=object_id, city_name=city)

    def update_to_sheet(self, id, city_name: str):
        city_code = flight_search.FlightSearch().get_iata_code(city_name=city_name)
        update: dict = {
            "price": {
                "iataCode": city_code
            }
        }
        response = requests.put(
            url=f"{EDIT_SHETTY_ENDPOINT}/{id}",
            json=update
        )
        response.raise_for_status()
        print(response.json())


