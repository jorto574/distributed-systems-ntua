from flask import Blueprint, current_app, request, jsonify
import traceback
from models.transaction import Transaction

validate_transaction_bp = Blueprint("validateTransaction", __name__)


@validate_transaction_bp.route("/validateTransaction", methods=["POST"])
def validate_transaction():
    try:
        data = request.json
        income_transaction = Transaction.from_dict(data["transaction"])
        my_wallet = current_app.config["my_wallet"]

        validated = my_wallet.validate_transaction(income_transaction)
        response_data = {}
        status_code = 0
        if validated:
            response_data = {"status": "success"}
            status_code = 200
        else:
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
