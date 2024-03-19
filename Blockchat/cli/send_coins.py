from server.utils.send_request import send_request

from server.models.transaction import Transaction


def send_coins(address, recipient_id, amount):

    print(f"Broadcasting {amount} to {recipient_id}")
    payload = {"recipient_id": recipient_id, "type": "coins", "body": amount}

    send_request("POST", address, "send_transaction", payload)
