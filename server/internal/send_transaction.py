from flask import Blueprint, request, jsonify, current_app
from utils.broadcast import broadcast
import threading 

from models.transaction import Transaction

send_transaction_bp = Blueprint("send_transaction", __name__)


@send_transaction_bp.route("/send_transaction", methods=["POST"])
def send_transaction():
    my_state = current_app.config["my_state"]

    data = request.json
    type = data["type"]
    body = data["body"]
    recipient_id = int(data["recipient_id"])

    if type == "message":
        amount = 0
        message = body
        recipient_public_key = my_state.wallets[recipient_id].public_key
    elif type == "coins":
        amount = int(body)
        message = ""
        recipient_public_key = my_state.wallets[recipient_id].public_key
    elif type == "stake":
        recipient_public_key = 0
        amount = int(body)
        message = ""

    new_transaction = my_state.my_wallet.create_transaction(
        my_state.my_wallet.public_key,
        recipient_public_key,
        type,
        amount,
        message,
        my_state.get_my_nonce(),
    )
    with my_state.lock:
        # print(threading.get_native_id())
        validated, response = my_state.validate_transaction(new_transaction)
        
    transaction_key = my_state.transaction_unique_id(new_transaction)

    if validated:
        # print(f"Broadcasting valid transaction with key {transaction_key}")
        success = broadcast(
            "validateTransaction",
            {"transaction": new_transaction.to_dict()},
            my_state.wallets,
            my_state.my_wallet.node_address,
        )
        if success:
            response += "\nSent to all nodes"
            # print(response)
        else:
            response += "\nBroadcast of transaction failed"
            # print(response)
    else:
        response += "\nTransaction was not broadcasted"
        # print(response)

    response_data = {}
    response_data = {"status": response}
    status_code = 200
    response = jsonify(response_data)

    return response, status_code
