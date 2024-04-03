from flask import Blueprint, current_app, request, jsonify
import traceback
from models.block import Block
import threading 

validate_block_bp = Blueprint("validateBlock", __name__)


@validate_block_bp.route("/validateBlock", methods=["POST"])
def validate_block():
    try:
        data = request.json
        incoming_block = Block.from_dict(data["block"])
        my_state = current_app.config["my_state"]
        node_id = my_state.my_wallet.node_id

        with my_state.lock:
            print(threading.get_native_id())
            block_validated = my_state.validate_block(incoming_block)
            if block_validated:
                blocks = list(my_state.block_waiting_room.values())
                my_state.block_waiting_room.clear()
                for block in blocks:
                    my_state.validate_block(block)
            
        
        response_data = {}
        status_code = 0

        if block_validated:
            # # my_state.block_waiting_room[incoming_block.index] = incoming_block
            # print(
            #     f"Node {node_id} validated the block with index = {incoming_block.index}"
            # )
            response_data = {"status": "success"}
            status_code = 200

        else:
            # print(
            #     f"Node {node_id} rejected the block with index = {incoming_block.index}"
            # )
            response_data = {"status": "failed"}
            status_code = 200

        response = jsonify(response_data)

        return response, status_code

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()  # Print the full traceback
        response_data = {"status": "failed", "error": str(e)}
        response = jsonify(response_data)

        return response, 500
