from flask import Blueprint, current_app, request, jsonify
import traceback
from models.block import Block

add_block_bp = Blueprint("addBlock", __name__)


@add_block_bp.route("/addBlock", methods=["POST"])
def add_block():
    try:
        data = request.json
        block_index = data["index"]
        my_state = current_app.config["my_state"]

        block = my_state.block_waiting_room[block_index]
        del my_state.block_waiting_room[block_index]
        my_state.add_block(block)
        my_state.update_transaction_inbox(block)

        response_data = {}

        print(f"Block with index = {block.index} added to blockchain")
        response_data = {"status": "success"}
        status_code = 200

        response = jsonify(response_data)

        return response, status_code

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()  # Print the full traceback
        response_data = {"status": "failed", "error": str(e)}
        response = jsonify(response_data)

        return response, 500
