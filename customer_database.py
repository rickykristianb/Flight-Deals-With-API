import requests
import os
from dotenv import load_dotenv

load_dotenv()

POST_CUST_ENDPOINT = os.getenv('POST_CUST_ENDPOINT')


class CustomerDatabase:

    def __init__(self):
        pass

    def save_customer_date(self, first_name: str, last_name: str, email: str):
        let_body = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
            }
        }

        response = requests.post(url=POST_CUST_ENDPOINT, json=let_body)
        response.raise_for_status()
        print(response.text)
