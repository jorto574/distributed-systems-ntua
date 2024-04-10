from server.utils.send_http_request import send_http_request
from server.models.transaction import Transaction


def send_message(address, recipient_id, body):

    print(f"Broadcasting 'message' transaction to {recipient_id}: {body}")
    payload = {"recipient_id": recipient_id, "type": "message", "body": body}

    response = send_http_request("POST", address, "send_transaction", payload)
    print(response["status"])
