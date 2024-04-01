from flask import Blueprint, current_app, jsonify
from utils.send_http_request import send_http_request
from utils.run_exp import run_exp
from time import time
import requests
import threading
import re


run_exp_bp = Blueprint("runExp", __name__)

@run_exp_bp("/runExp", methods=["GET"])
def run_exp():
    my_state = current_app.config["my_state"]
    node_id = my_state.my_wallet.node_id
    node_address = my_state.node_address

    bootstrap_addr = my_state.wallets[0].node_address

    threading.Thread(target=run_exp, args=(node_id, node_address, bootstrap_addr)).start()
    
    response_data = {"status": "success"}
    response_status = 200

    return jsonify(response_data), response_status

    