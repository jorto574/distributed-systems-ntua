from server.utils.send_request import send_request

from server.models.transaction import Transaction


def send_message(address, recipient_id, body):

    # check if trasaction type is "message"
    if body[0] == '"':
        print(f"Broadcasting 'message' transaction to {recipient_id}: {body[1:-1]}")
        payload = {"recipient_id": recipient_id, "type": "message", "body": body[1:-1]}
    else:  # transaction is type "coins"
        print(f"Broadcasting 'coins' transaction to {recipient_id}: {body} BCC ")
        payload = {"recipient_id": recipient_id, "type": "coins", "body": body}

    response = send_request("POST", address, "send_transaction", payload)
    print(response)
