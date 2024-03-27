from flask import Blueprint, current_app, request, jsonify
import traceback
from models.transaction import Transaction

validate_transaction_bp = Blueprint("validateTransaction", __name__)


@validate_transaction_bp.route("/validateTransaction", methods=["POST"])
def validate_transaction():
    try:
        data = request.json
        incoming_transaction = Transaction.from_dict(data["transaction"])
        my_state = current_app.config["my_state"]
        node_id = my_state.my_wallet.node_id
        receiver_id = my_state.find_wallet_from_public_key(
            incoming_transaction.receiver_public_key
        ).node_id

        key = my_state.transaction_unique_id(incoming_transaction)

        if key in my_state.blockchain.blockchain_transactions:
            response_data = {"status": "transaction already in blockchain"}
            response = jsonify(response_data)
            status_code = 200
            return response, status_code

        transaction_validated = my_state.validate_transaction(incoming_transaction)
        response_data = {}
        status_code = 0

        if transaction_validated:
            print(
                f"Node {node_id} validated the transaction with (sender_id,nonce) = {key}"
            )
            response_data = {"status": "success"}
            status_code = 200

        else:
            print(
                f"Node {node_id} rejected the transaction with (nonce, sender_public_key) = ({incoming_transaction.nonce}, {incoming_transaction.sender_public_key})"
            )
            response_data = {"status": "failed"}
            status_code = 401

        response = jsonify(response_data)

        return response, status_code

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()  # Print the full traceback
        response_data = {"status": "failed", "error": str(e)}
        response = jsonify(response_data)

        return response, 500
