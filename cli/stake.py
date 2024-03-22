from server.utils.send_http_request import send_http_request

from server.models.transaction import Transaction


def stake(amount):
    # Implement your logic for staking a certain amount
    print(f"Staking {amount} coins")
    recipient_id = None  # TODO
    payload = {"recipient_id": recipient_id, "stake_value": amount}

    address = None  # TODO
    send_http_request("POST", address, "set_stake", payload)


def current_stake():
    stake = 10
    address, payload = None, None  # TODO
    send_http_request("POST", address, "view_stake", payload)
