from flask import Blueprint, request, current_app, jsonify
from utils.broadcast import broadcast
import time

exp_signal_bp = Blueprint("exp_signal", __name__)

@exp_signal_bp.route("/exp_signal", methods=["GET"])
def exp_signal():
    my_state = current_app.config["my_state"]
    wallets = my_state.wallets 
    my_wallet = my_state.my_wallet
    current_app.config["start_time"] = time.time()
    current_app.config["node_count"] = 0

    broadcast(
            "/runExp",
            {},
            wallets,
            None, # trigerring run_exp to node0 as well
        )

    response_data = {"status": "Test started. Go to server terminal of Node 0 to see results."}
    response_status = 200

    return jsonify(response_data), response_status
