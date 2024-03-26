from flask import Blueprint, current_app, jsonify

view_bp = Blueprint("view", __name__)


@view_bp.route("/view", methods=["GET"])
def view():
    my_state = current_app.config["my_state"]

    last_block_dict = my_state.blockchain.block_list[-1].to_dict()
    last_block_dict["validator_id"] = my_state.public_key_to_node_id[
        tuple(last_block_dict["validator"])
    ]

    response_data = {"last_block": last_block_dict}
    response = jsonify(response_data)
    status_code = 200

    return response, status_code
