from flask import Blueprint, request, current_app, jsonify

balance_bp = Blueprint("balance", __name__)


@balance_bp.route("/balance", methods=["GET"])
def balance():
    wallets = current_app.config["my_state"].wallets_serialization()

    response_data = {"wallets": wallets}
    response_status = 200

    return jsonify(response_data), response_status
