import os
import vonage


def get_creds():
    url = os.environ.get("url_for_us")
    email = os.environ.get("email_for_us")
    password = os.environ.get("password_for_us")

    return email, password, url


def send_sms(messages):
    api_key = os.environ.get("vonage_api_key")
    secret = os.environ.get("vonage_secret_key")
    client = vonage.Client(key=api_key, secret=secret)
    sms = vonage.Sms(client)
    response = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "15147751622",
            "text": "This is a test function call",
        }
    )
    if response["messages"][0]["status"] == "0":
        print("Message sent successfully.")
        return True
    else:
        print(f"Message failed with error: {response['messages'][0]['error-text']}")
        return False
