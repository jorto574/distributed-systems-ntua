from flask import Blueprint, request, jsonify, current_app

send_transaction_bp = Blueprint("send_transaction", __name__)


@send_transaction_bp.route("/send_transaction", methods=["POST"])
def send_transaction():
    my_state = current_app.config["my_state"]

    data = request.json

    breakpoint()

    return "Server of Blockchat Node is up and running"
