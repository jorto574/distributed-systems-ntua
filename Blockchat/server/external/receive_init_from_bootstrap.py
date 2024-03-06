from flask import Blueprint, request, jsonify, current_app

from models.blockchain import Blockchain
from models.state import State

receive_init_from_bootstap_bp = Blueprint("receiveInitFromBootstrap", __name__)


@receive_init_from_bootstap_bp.route("/receiveInitFromBootstrap", methods=["POST"])
def receive_init_from_bootstap():
    node_num = current_app.config["node_num"]
    try:

        data = request.json

        blockchain = Blockchain.from_dict(data["blockchain"])
        wallets = State.wallets_from_dict(data["wallets"])
        current_app.config["my_state"] = State(blockchain, wallets, node_num)

        response_data = {"status": "success"}
        response = jsonify(response_data)

        print("Blockchat initalization succesfull - all nodes online.")

        return response, 200

    except Exception as e:
        print(f"An error occurred: {e}")
        response_data = {"status": "failed", "error": str(e)}
        response = jsonify(response_data)

        return response, 500
