from flask import Flask, request, jsonify
from transaction import Transaction
from node import Node
from state import State
from block import Block
from blockchain import Blockchain
from my_wallet import MyWallet
from wallet import Wallet
import time
import requests

app = Flask(__name__)

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

my_state = None

@app.route('/receiveIpsPortsPksFromBootstrap', methods=['POST'])
def receive_ips_ports_pks_from_bootsrap():
    global my_state
    try:
        request_data = request.get_json()
        print("request_data")
        print(request_data)

        received_blockchain = request_data[1]["blockchain"]
        received_blocks_list = received_blockchain["blocks"]
        my_blockchain = Blockchain([])

        # reconstruct the blockcain
        for block in received_blocks_list:
            new_block = Block(block["index"], block["timestamp"], [], block["validator"], block["current_hash"], block["previous_hash"])
            for transaction in block["transactions"]:
                new_transaction = Transaction(transaction["sender_address"], transaction["receiver_address"], transaction["type_of_transaction"], transaction["amount"], transaction["message"], transaction["signature"])
                new_block.add_transaction(new_transaction)
            my_blockchain.add_block(new_block)

        my_state = State(my_blockchain, [], [], [])
        print(my_state)
        # gather all nodes
        received_nodes_list = request_data[0]["nodes"]
        for i in range (0, len(received_nodes_list)):
            node_public_key = received_nodes_list[i]["node_public_key"]["first"], received_nodes_list[i]["node_public_key"]["second"]
            node = Node(received_nodes_list[i]["node_id"], received_nodes_list[i]["ip_address"], received_nodes_list[i]["port"], node_public_key)
            #wallet = Wallet(node_public_key, )
            my_state.add_node(node)

        response_data = {
            "status": "success"
        }
        response = jsonify(response_data)

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
    app.run(debug=True, port=3001)