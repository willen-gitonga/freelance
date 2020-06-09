import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64



class MpesaC2bCredential:
    consumer_key = 'VUAyuB3eAYjKLw3sD2qhwpKVe6pQaCGj'
    consumer_secret = 'fQiSQ4M8lEd6BCZL'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

class LipanaMpesaPpassword:
    Test_c2b_shortcode = "600000"

