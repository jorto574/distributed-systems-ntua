from flask import Blueprint, request, jsonify, after_this_request, current_app
import threading
import traceback

from models.wallet import PublicWallet
from models.transaction import Transaction

from utils.broadcast import broadcast


talk_to_bootstrap_bp = Blueprint("talkToBootstrap", __name__)


# when a node enters, it must send a request to this url so that the bootstrap sends him his unique node_id
@talk_to_bootstrap_bp.route("/talkToBootstrap", methods=["POST"])
def talk_to_bootstrap():
    my_state = current_app.config["my_state"]
    wallets = my_state.wallets
    my_wallet = my_state.my_wallet
    bootstrap_addr = current_app.config["bootstrap_addr"]
    # is_bootstrap = current_app.config['is_bootstrap']

    try:
        current_app.config["node_count"] += 1
        node_id = current_app.config["node_count"]

        request_data = request.get_json()
        node_public_key = request_data.get("public_key")
        node_address = request_data.get("address")

        new_transaction = my_wallet.create_transaction(
            my_wallet.public_key,
            node_public_key,
            "coins",
            1000,
            f"Welcome to Blockchat node {node_id}",
        )

        my_state.add_transaction(new_transaction)

        my_state.wallets[0].amount -= 1000
        node_wallet = PublicWallet(node_id, node_address, node_public_key, 1000)
        my_state.add_wallet(node_wallet)

        response_data = {"status": "success", "id": node_id}

        node_num = current_app.config["node_num"]
        node_count = current_app.config["node_count"]
        response = jsonify(response_data)
        if (node_count + 1) == node_num:
            # the bootstrap node broadcasts to every other node all the ips, ports and public keys of other nodes
            threading.Thread(
                target=broadcast,
                args=(
                    # endpoint
                    "receiveInitFromBootstrap",
                    # payload
                    {
                        "blockchain": my_state.blockchain.to_dict(),
                        "wallets": my_state.wallets_serialization(),
                    },
                    wallets,
                    bootstrap_addr,
                ),
            ).start()

        return response, 200

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()  # Print the full traceback
        response_data = {"status": "failed", "error": str(e)}
        response = jsonify(response_data)

        return response, 500
