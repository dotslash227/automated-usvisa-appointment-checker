#!/usr/bin/python3

import os
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)


def get_creds():
    url = os.environ.get("url_for_us")
    email = os.environ.get("email_for_us")
    password = os.environ.get("password_for_us")

    return email, password, url


def send_sms(status_dict):
    if status_dict is None:
        append_message = "No slots available in Montreal or Quebec City or Toronto :("
    else:
        append_message = (
            f"Montreal : {status_dict.get('Montreal')} \n Quebec City : {status_dict.get('Quebec City')} "
            f"\n Toronto : {status_dict.get('Toronto')}"
        )
    message_to_be_sent = (
        f"Bonjour Dr. Mehak, I am your automated US visa appointment checker and "
        f"here's the update on the most recent run. \n"
        f" {append_message}"
    )
    sid = os.environ.get("twilio_sid")
    auth = os.environ.get("twilio_auth")
    from_number = os.environ.get("us_from_number")
    to_number = os.environ.get("us_to_number")
    client = Client(sid, auth)
    message = client.messages.create(
        body=message_to_be_sent, from_=from_number, to=to_number
    )
    logger.info(f"SMS sent with SMS id: {message.sid}")
    return message.sid
