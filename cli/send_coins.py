from server.utils.send_http_request import send_http_request

from server.models.transaction import Transaction


def send_coins(address, recipient_id, amount):

    print(f"Broadcasting {amount} to {recipient_id}")
    payload = {"recipient_id": recipient_id, "type": "coins", "body": amount}

    response = send_http_request("POST", address, "send_transaction", payload)
    print(response["status"])
