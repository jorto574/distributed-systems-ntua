from server.utils.send_request import send_request

from server.models.transaction import Transaction


def send_message(address, recipient_id, body):

    print(f"Broadcasting 'message' transaction to {recipient_id}: {body}")
    payload = {"recipient_id": recipient_id, "type": "message", "body": body}

    send_request("POST", address, "send_transaction", payload)
