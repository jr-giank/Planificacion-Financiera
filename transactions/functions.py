

import requests
from requests.auth import HTTPBasicAuth

import os

from dotenv import load_dotenv

load_dotenv()

MOOV_API_KEY = os.getenv('PUBLIC_KEY')
MOOV_SECRET_KEY = os.getenv('MV_SECRET_KEY')

print(f"\n\nApi 1: {MOOV_API_KEY}\n\n")

print(f"\n\nApi 2: {MOOV_SECRET_KEY}\n\n")


def get_moov_token():

    token_response = requests.post(
        "https://api.moov.io/oauth2/token",
        auth=HTTPBasicAuth(MOOV_API_KEY, MOOV_SECRET_KEY),
        data={"grant_type": "client_credentials", "scope": "/accounts.write"}
    )

    # print("Token Response Status:", token_response.status_code)
    # print("Token Response Headers:", token_response.headers)
    # print("Token Response Content:", token_response.text)

    token_data = token_response.json() if token_response.status_code == 200 else {}
    access_token = token_data.get("access_token")
    print("Access Token:", access_token)

    return token_data.get("access_token")