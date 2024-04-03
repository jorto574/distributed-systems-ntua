from flask import Blueprint, current_app, request, jsonify
import traceback
from models.transaction import Transaction
import threading

validate_transaction_bp = Blueprint("validateTransaction", __name__)


@validate_transaction_bp.route("/validateTransaction", methods=["POST"])
def validate_transaction():
    try:
        data = request.json
        incoming_transaction = Transaction.from_dict(data["transaction"])
        my_state = current_app.config["my_state"]
        node_id = my_state.my_wallet.node_id

        key = my_state.transaction_unique_id(incoming_transaction)

        # check if transaction has already been sent as part of a minted block
        if key in my_state.blockchain.blockchain_transactions: 
            del my_state.blockchain.blockchain_transactions[key]
            response_data = {"status": "transaction already in blockchain"}
            response = jsonify(response_data)
            status_code = 200
            return response, status_code

        with my_state.lock:
            print(threading.get_native_id(), my_state.lock)
            _ = my_state.validate_transaction(incoming_transaction)
            

        # print(
        #         f"Node {node_id} received the transaction with (sender_id,nonce) = {key}"
        # )

        response_data = {}
        response_data = {"status": "success"}
        status_code = 200
        response = jsonify(response_data)

        return response, status_code

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()  # Print the full traceback
        response_data = {"status": "failed", "error": str(e)}
        response = jsonify(response_data)

        return response, 500
