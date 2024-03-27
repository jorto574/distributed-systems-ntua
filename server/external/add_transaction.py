from flask import Blueprint, request, current_app, jsonify
from models.transaction import Transaction
import threading

add_transaction_bp = Blueprint("add_transaction", __name__)


@add_transaction_bp.route("/addTransaction", methods=["POST"])
def add_transaction():
    my_state = current_app.config["my_state"]
    data = request.json
    transaction_key = tuple(data["transaction_key"])
    if transaction_key in my_state.blockchain.blockchain_transactions:
        del my_state.blockchain.blockchain_transaction[transaction_key]
        response_data = {"status": "transaction already in blockchain"}
        response = jsonify(response_data)
        status_code = 200
        return response, status_code

    my_state.add_transaction(transaction_key)
    my_state.stakes

    response = {"status": f"Transaction {transaction_key} added to transaction inbox"}
    status_code = 200

    return response, status_code
