from flask import Blueprint, current_app, jsonify
from utils.send_http_request import send_http_request
from utils.run_exp import run_exp_backend
from time import time
import requests
import threading
import re


run_exp_bp = Blueprint("runExp", __name__)

@run_exp_bp.route("/runExp", methods=["POST"])
def run_exp():
    my_state = current_app.config["my_state"]
    node_id = my_state.my_wallet.node_id
    node_address = my_state.my_wallet.node_address
    node_num = current_app.config["node_num"]

    bootstrap_addr = my_state.wallets[0].node_address

    threading.Thread(target=run_exp_backend, args=(node_id, node_address, bootstrap_addr, node_num)).start()
    
    response_data = {"status": "success"}
    response_status = 200

    return jsonify(response_data), response_status

    