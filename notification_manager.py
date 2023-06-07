import smtplib

import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_NUM = os.getenv('TWILIO_NUM')
GET_USER_SHEETY_ENDPOINT = os.getenv('GET_USER_SHEETY_ENDPOINT')
EMAIL = os.getenv('EMAIL')
PASSRWORD = os.getenv('PASSWORD')


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.route_status = False

    def send_notification(self, price, departure_city, departure_iatacode, arrival_city, arrival_iatacode, outbound_date, inbound_date, route_city):
        route_city_list = [route_detail["cityTo"] for index, route_detail in enumerate(route_city) if index < len(route_city) - 1]
        route_len = len(route_city_list)
        print(route_city_list)
        print(route_len)
        if route_len > 1:
            self.route_status = True
            route_city = ", ".join(route_city_list)

        client = Client(TWILIO_SID, TWILIO_TOKEN)
        if self.route_status:
            message = client.messages \
                .create(
                body=f"Low price alert! Only USD{price} to fly from {departure_city}-{departure_iatacode} to "
                     f"{arrival_city}-{arrival_iatacode}, from {outbound_date} to {inbound_date}\nFlight has "
                     f"{route_len} stop over, via {route_city}",
                from_=TWILIO_NUM,
                to='+6282168897862'

            )
        else:
            message = client.messages \
                .create(
                body=f"Low price alert! Only USD{price} to fly from {departure_city}-{departure_iatacode} to "
                     f"{arrival_city}-{arrival_iatacode}, from {outbound_date} to {inbound_date}",
                from_=TWILIO_NUM,
                to='+6282168897862'
            )
        print(message.sid)

    def send_email(self, price, departure_city, departure_iatacode, arrival_city, arrival_iatacode, outbound_date, inbound_date):
        response = requests.get(url=GET_USER_SHEETY_ENDPOINT)
        response.raise_for_status()
        data = response.json()["users"]
        google_flight_link = "https://www.google.co.uk/flights?hl=en#flt="
        for user_email in data:
            with smtplib.SMTP(host="smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=EMAIL,password=PASSRWORD)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=user_email["email"],
                    msg=f"Subject:New Low Price Flight!!\n\nLow price alert! Only ${price} to fly from "
                        f"{departure_city}-{departure_iatacode} to {arrival_city}-{arrival_iatacode}, "
                        f"from {outbound_date} to {inbound_date}\n\nClick link below to open in google "
                        f"flight\n{google_flight_link}{departure_iatacode}.{arrival_iatacode}.{outbound_date}"
                )