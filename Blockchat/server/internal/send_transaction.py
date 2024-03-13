from flask import Blueprint, request, jsonify, current_app

from models.transaction import Transaction

send_transaction_bp = Blueprint("send_transaction", __name__)


@send_transaction_bp.route("/send_transaction", methods=["POST"])
def send_transaction():
    my_state = current_app.config["my_state"]

    data = request.json
    type = data["type"]
    body = data["body"]
    recipient_id = int(data["recipient_id"])
    recipient_public_key = my_state.wallets[recipient_id].public_key

    if type == "message":
        amount = 0
        message = body
    else:
        amount = int(body)
        message = ""

    new_transaction = my_state.my_wallet.create_transaction(
        my_state.my_wallet.public_key, recipient_public_key, type, amount, message
    )
    breakpoint()
    # TODO: validate and broadcast transaction

    print(data)
    return "Transaction broadcasted to all nodes"
