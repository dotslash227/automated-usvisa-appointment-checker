import os
import random
from motivations import motivation_quotes
from twilio.rest import Client


def get_creds():
    url = os.environ.get("url_for_us")
    email = os.environ.get("email_for_us")
    password = os.environ.get("password_for_us")

    return email, password, url


def send_sms(status_dict):
    random_number = random.randint(0, 4)
    message_to_be_sent = (
        f"Bonjour Dr. Mehak, I am your automated US visa appointment checker and "
        "here's the update for the most recent run. \n"
        f"Montreal : {status_dict.get('Montreal')} \n"
        f"Quebec City : {status_dict.get('Quebec City')} \n"
        f"Toronto : {status_dict.get('Toronto')} \n"
        f"Who's the smartest? Dr. Mehak Khanna is the smartest, she's a genius."
        "40% BTC, 40% ETH, 10% USDC, 10% SOL"
        f"\n{motivation_quotes[random_number]} "
    )

    sid = os.environ.get("twilio_sid")
    auth = os.environ.get("twilio_auth")
    from_number = os.environ.get("us_from_number")
    to_number = os.environ.get("us_to_number")
    client = Client(sid, auth)
    message = client.messages.create(
        body=message_to_be_sent, from_=from_number, to=to_number
    )
    return message.sid
