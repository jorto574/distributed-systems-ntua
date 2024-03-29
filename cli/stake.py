import os
from dotenv import load_dotenv

from server.utils.send_http_request import send_http_request

from server.models.transaction import Transaction

load_dotenv(f"{os.path.dirname(os.path.abspath(__file__))}/config.env")


def stake(address, amount):
    print(f"Staking {amount} BCC")
    payload = {"recipient_id": -1, "type": "stake", "body": amount}
    response = send_http_request("POST", address, "send_transaction", payload)
    print(response["status"])
    # response = send_http_request("POST", address, "stake", {"stake_value": amount})


# def current_stake():
#     address, payload = None, None  # TODO
#     payload = {}
#     send_http_request("POST", address, "stake/view", payload)
