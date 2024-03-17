from flask import Blueprint, current_app

validate_transaction_bp = Blueprint("validateTransaction",  __name__)

@validate_transaction_bp.route("/validateTransaction", methods=["POST"])
def validate_transaction():
