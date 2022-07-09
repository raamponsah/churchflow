# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC30f4810cbe11cb2539cf88ee250a6e9e'
auth_token = '8d011dd4578816862bfbffe366a520ef'
client = Client(account_sid, auth_token)


def send_sms(**kwargs):
    try:
        message = client.messages \
            .create(
            body=f"{kwargs['message_content']}",
            from_='+17404957241',
            to=f"{kwargs['sendto']}"
        )
        print(f"{kwargs['sendto']} {kwargs['message_content']}")
    except Exception as e:
        print(e)