from flask import Flask, request, jsonify, after_this_request, session
from dotenv import load_dotenv, dotenv_values
from my_wallet import MyWallet
from wallet import Wallet
from state import State
from init_bootstrap import init_bootstrap
from node import Node
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
load_dotenv()

BASE_URL = os.environ.get("BASE_URL")
PORT = os.environ.get("PORT")
print(PORT)

@app.route('/')
def hello_world():
    return 'Hello, World! This is a Flask server.'


@app.route('/validateTransaction', methods=['POST'])
def validate_transaction():
    if not request.is_json:
        return jsonify({"error": "Invalid request, must provide JSON data"}), 400
    
    transaction_data = request.get_json()
    transaction = transaction_data['transaction']

    return

@app.route('/validateBlock', methods=['POST'])
def validate_block():
    if not request.is_json:
        return jsonify({"error": "Invalid request, must provide JSON data"}), 400
    
    block_data = request.get_json()
    block = block_data['block']

    return


@app.route('/receiveMessage')
def receive_message():
    transaction_kind = request.args.get('transaction_kind', '')
    return

node_id = 0
# when a node enters, it must send a request to this url so that the bootstrap sends him his unique node_id
@app.route('/talkToBootstrap', methods=['GET', 'POST'])
def talk_to_bootstrap():
    global my_state

    # here the bootstrap node broadcasts to every other node all the ips, ports and public keys of other nodes
    def broadcast_ips_ports_pks(num_nodes, my_state):
        url = "http://127.0.0.1"
        port = 3000
        payload = [{
            "nodes": [] 
        }]

        # create the request body
        for i in range (0, num_nodes + 1):
            node_public_key = my_state.get_wallets()[i].get_public_key()
            payload[0]["nodes"].append({
                "node_id": i,
                "ip_address": url,
                "port": port,
                "node_public_key": {
                    "first": node_public_key[0],
                    "second": node_public_key[1]
                }
            })
            if i >= 1:
                new_node = Node(i, url, port, node_public_key)
                my_state.add_node(new_node)
            port += 1
        
        session['state'] = 1324234234
        # add to the request body the blockchain, so that it can be broadcasted to each node
        blockchain_dict = my_state.get_blockchain().to_dict()
        payload.append({
            "blockchain": blockchain_dict
        })
        # send http request to each other node
        port = 3001
        for i in range (1, num_nodes + 1):
            try:
                response = requests.post(f"{url}:{port}/receiveIpsPortsPksFromBootstrap", json = payload)
                port += 1

                if response.status_code == 200:
                    print("Successfully broadcasted to every node!")
                else:
                    print(f"Request failed with status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Error making the request: {e}")

    try:
        global node_id
        node_id += 1

        request_data = request.get_json()
        node_public_key = request_data.get("public_key")
        print(node_public_key)
        node_wallet = Wallet(node_public_key, 0)
        my_state.add_wallet(node_wallet)

        response_data = {
            "status": "success",
            "id": node_id
        }
        response = jsonify(response_data)

        @after_this_request
        def after_response(response):
            if node_id == 1:
                broadcast_ips_ports_pks(node_id, my_state)
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


if __name__ == '__main__':
    print("started boot")
    my_state = init_bootstrap()
    app.run(debug=True, port=3000)