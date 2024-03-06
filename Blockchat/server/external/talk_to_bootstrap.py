from flask import Blueprint, request, jsonify, after_this_request, current_app
import requests
import threading

from models.wallet import Wallet
from models.transaction import Transaction


talk_to_bootstrap_bp = Blueprint("talkToBootstrap", __name__)


# the bootstrap node broadcasts to every other node all the ips, ports and public keys of other nodes
def broadcast_ips_ports_pks(bootstrap_addr, my_state):

    blockchain_dict = my_state.get_blockchain().to_dict()
    wallets_dict = my_state.wallets_to_dict()

    payload = {"blockchain": blockchain_dict, "wallets": wallets_dict}

    success = True
    # send http request to each node
    for address in my_state.wallets.keys():
        if address != bootstrap_addr:
            node_id = my_state.wallets[address].node_id
            try:
                response = requests.post(
                    f"http://{address}/receiveInitFromBootstrap", json=payload
                )
                if response.status_code == 200:
                    print(f"Successfully broadcasted Blockchat to node {node_id}.")
                else:
                    success = False
                    print(
                        f"Broadcast to node {node_id} failed with status code: {response.status_code}"
                    )

            except requests.exceptions.RequestException as e:
                print(f"Error making the request: {e}")

    if success:
        print(f"Successfully broadcasted Blockchat to every node!")


# when a node enters, it must send a request to this url so that the bootstrap sends him his unique node_id
@talk_to_bootstrap_bp.route("/talkToBootstrap", methods=["POST"])
def talk_to_bootstrap():
    my_state = current_app.config["my_state"]
    bootstrap_addr = current_app.config["bootstrap_addr"]
    # is_bootstrap = current_app.config['is_bootstrap']

    try:
        current_app.config["node_count"] += 1
        node_id = current_app.config["node_count"]

        request_data = request.get_json()
        node_public_key = request_data.get("public_key")
        node_address = request_data.get("address")

        new_transaction = Transaction(
            bootstrap_addr,
            node_address,
            "coins",
            1000,
            f"Welcome to Blockchat node {node_id}",
            None,
        )
        # TODO: add signature to transaction
        my_state.blockchain.add_transaction(new_transaction)

        my_state.wallets[bootstrap_addr].amount -= 1000
        node_wallet = Wallet(node_id, node_address, node_public_key, 1000)
        my_state.add_wallet(node_address, node_wallet)

        response_data = {"status": "success", "id": current_app.config["node_count"]}

        node_num = current_app.config["node_num"]
        node_count = current_app.config["node_count"]
        response = jsonify(response_data)
        if (node_count + 1) == node_num:
            threading.Thread(
                target=broadcast_ips_ports_pks, args=(bootstrap_addr, my_state)
            ).start()

        return response, 200

    except Exception as e:
        print(f"An error occurred: {e}")
        response_data = {"status": "failed", "error": str(e)}
        response = jsonify(response_data)
        return response, 500
