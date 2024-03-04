from flask import Blueprint, request, jsonify, after_this_request, current_app
import requests

from models.wallet import Wallet

talk_to_bootstrap_bp = Blueprint('talkToBootstrap', __name__)

# the bootstrap node broadcasts to every other node all the ips, ports and public keys of other nodes
def broadcast_ips_ports_pks(bootstrap_addr,my_state):

    blockchain_dict = my_state.get_blockchain().to_dict()
    wallets_dict = my_state.wallets_to_dict()

    payload = [{
        "blockchain": blockchain_dict,
        "wallets": wallets_dict
    }]

    # send http request to each node
    for address in my_state.wallets.keys():
        if address != bootstrap_addr: 
            try:
                response = requests.post(f"http://{address}/receiveInitFromBootstrap", json = payload)
                if response.status_code == 200:
                    print("Successfully broadcasted to every node!")
                else:
                    print(f"Request failed with status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Error making the request: {e}")

# when a node enters, it must send a request to this url so that the bootstrap sends him his unique node_id
@talk_to_bootstrap_bp.route('/talkToBootstrap', methods=['POST'])
def talk_to_bootstrap():
    my_state = current_app.config['my_state']
    bootstrap_addr = current_app.config['bootstrap_addr']
    is_bootstrap = current_app.config['is_bootstrap']
    node_num = current_app.config['node_num']
    node_count = 0

    if is_bootstrap != "1":
        return "Not Bootstrap Node"
    
    try:
        node_count += 1

        request_data = request.get_json()
        node_public_key = request_data.get("public_key")
        node_address = request_data.get("address")
        my_state.wallets[bootstrap_addr].amount -= 1000
        node_wallet = Wallet(node_count,node_address,node_public_key, 1000)
        my_state.add_wallet(node_address,node_wallet)

        response_data = {
            "status": "success",
            "id": node_count
        }
        response = jsonify(response_data)

        @after_this_request
        def after_response(response):
            if (node_count +1) == node_num:
                broadcast_ips_ports_pks(bootstrap_addr,my_state)
            return response

        return response, 200
    
    except Exception as e:
        print(f"An error occurred: {e}")
        response_data = {
            "status": "failed",
            "error": str(e)  
        }
        response = jsonify(response_data)
        return response, 500