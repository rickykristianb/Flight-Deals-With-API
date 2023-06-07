# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import data_manager
import flight_search
import notification_manager
from datetime import datetime as dt, timedelta as td
import customer_database
import notification_manager


def main():
    is_insertcust = True
    cust_data = customer_database.CustomerDatabase()
    while is_insertcust:
        insert_data = input("Do you have a new customer to save? Y/N: ").lower()
        if insert_data == "n":
            break
        email = ""
        first_name_in = input("Insert First Name: ")
        last_name_in = input("Insert last Name: ")
        is_email_false = True
        while is_email_false:
            email = input("Insert Email: ")
            if "@" in email and "." in email:
                is_email_false = False
            else:
                print("Email is not correct")
        is_confirm_email_false = True
        while is_confirm_email_false:
            email_confirm = input("Type your email again: ")
            if email_confirm == email:
                is_confirm_email_false = False
                cust_data.save_customer_date(first_name=first_name_in, last_name=last_name_in, email=email)
            else:
                print("Email is not same")
        add_cust = input("Have another customer to save? Y/N: ").lower()
        if add_cust == "n":
            is_insertcust = False

    get_data = data_manager.DataManager()
    data = get_data.get_sheets_data()
    get_data.set_iatacode()
    send_email = notification_manager.NotificationManager()

    flight = flight_search.FlightSearch()
    fly_from_input = input("From: ")

    date_now = dt.now()
    date_from = (date_now + td(1)).strftime("%d/%m/%Y")
    date_to = (date_now + td(60)).strftime("%d/%m/%Y")
    date_from_togoogle = (date_now + td(1)).strftime("%Y-%m-%d")

    fly_from_iatacode = flight.get_iata_code(city_name=fly_from_input)
    for detail in data:
        flight_detail = flight.search_flight(date_from=date_from, date_to=date_to, fly_from=fly_from_iatacode, fly_to=detail["iataCode"])

        if flight_detail is not None:
            route = flight_detail["data"][0]["route"]
            price = flight_detail["data"][0]["price"]
            print(f"{detail['city']}: ${price}")
            notification_config = notification_manager.NotificationManager()

            if price < detail["lowestPrice"]:
                notification_config.send_notification(
                    price=price,
                    departure_city=fly_from_input,
                    departure_iatacode=fly_from_iatacode,
                    arrival_city=detail["city"],
                    arrival_iatacode=detail["iataCode"],
                    outbound_date=date_from,
                    inbound_date=date_to,
                    route_city=route,
                )
                send_email.send_email(
                    price=price,
                    departure_city=fly_from_input,
                    departure_iatacode=fly_from_iatacode,
                    arrival_city=detail["city"],
                    arrival_iatacode=detail["iataCode"],
                    outbound_date=date_from_togoogle,
                    inbound_date=date_to
                )
        else:
            continue


if __name__ == main():
    main()
