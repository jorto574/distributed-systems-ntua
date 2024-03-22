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

        # TODO: continue work
        # sender_public_key = tuple(incoming_transaction.sender_public_key)
        # nonce = incoming_transaction.nonce
        key = (sender_public_key, nonce)

        if key in my_state.blockchain.blockchain_transactions:
            del my_state.blockchain.blockchain_transaction
            response_data = {"status": "transaction already in blockchain"}
            response = jsonify(response_data)
            status_code = 200
            return response, status_code

        transaction_validated = my_state.validate_transaction(incoming_transaction)
        response_data = {}
        status_code = 0

        # TODO: continue work
        # sender_id = my_state.public_key_to_node_id[transaction]
        if transaction_validated:
            print(
                f"Node {node_id} validated the transaction with (nonce, sender_id) = ({incoming_transaction.nonce}, {sender_id})"
            )
            response_data = {"status": "success"}
            status_code = 200

            if node_id == receiver_id:
                print(
                    f"You've received a transaction of type {incoming_transaction.type_of_transaction}"
                )
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
