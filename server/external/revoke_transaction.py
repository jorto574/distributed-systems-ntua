from flask import Blueprint, request, current_app

revoke_transaction_bp = Blueprint("revokeTransaction", __name__)


@revoke_transaction_bp.route("/revokeTransaction", methods=["POST"])
def revoke_transaction():
    my_state = current_app.config["my_state"]

    transaction = request.json["transaction"]

    sender_address = tuple(transaction.sender_address)
    nonce = transaction.nonce
    key = (sender_address, nonce)

    del my_state.blockchain.transaction_inbox[key]

    response = {"status": "Transaction revoked"}
    status_code = 200

    return response, status_code
