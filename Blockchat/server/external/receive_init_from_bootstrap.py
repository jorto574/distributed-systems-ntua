from flask import Blueprint, request, jsonify, current_app

from models.state import State
from models.block import Block
from models.blockchain import Blockchain
from models.transaction import Transaction

receive_init_from_bootstap_bp = Blueprint('receiveInitFromBootstrap', __name__)

@receive_init_from_bootstap_bp.route('/receiveInitFromBootstrap', methods=['POST'])
def receive_init_from_bootstap_bp():

    try:
        data = request.json
        print("request_data")
        print(data)
        breakpoint()

        # received_blockchain = request_data[1]["blockchain"]
        # received_blocks_list = received_blockchain["blocks"]
        # my_blockchain = Blockchain([])

        # # reconstruct the blockcain
        # for block in received_blocks_list:
        #     new_block = Block(block["index"], block["timestamp"], [], block["validator"], block["current_hash"], block["previous_hash"])
        #     for transaction in block["transactions"]:
        #         new_transaction = Transaction(transaction["sender_address"], transaction["receiver_address"], transaction["type_of_transaction"], transaction["amount"], transaction["message"], transaction["signature"])
        #         new_block.add_transaction(new_transaction)
        #     my_blockchain.add_block(new_block)

        # my_state = State(my_blockchain, [], [], [])

        # # gather all nodes
        # received_nodes_list = request_data[0]["nodes"]
        # for i in range (0, len(received_nodes_list)):
        #     node_public_key = received_nodes_list[i]["node_public_key"]
        #     node = Node(received_nodes_list[i]["node_id"], received_nodes_list[i]["ip_address"], received_nodes_list[i]["port"], node_public_key)
        #     #wallet = Wallet(node_public_key, )
        #     my_state.add_node(node)

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