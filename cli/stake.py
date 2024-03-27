import os
from dotenv import load_dotenv

from server.utils.send_http_request import send_http_request

from server.models.transaction import Transaction

load_dotenv(f"{os.path.dirname(os.path.abspath(__file__))}/config.env")

def stake(amount, address, debug:bool = False):
    if debug:
        print(f"Staking {amount} coins")
    response = send_http_request("POST", address, "stake/set", {"stake_value": amount})


def current_stake():
    address, payload = None, None  # TODO
    payload = {}
    send_http_request("POST", address, "stake/view", payload)
