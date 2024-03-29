from flask import Blueprint, current_app

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home():
    my_state = current_app.config["my_state"]
    node_id = my_state.my_wallet.node_id
    return f"Server of Blockchat Node {node_id} is up and running"
