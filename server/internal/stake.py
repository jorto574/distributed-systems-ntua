from flask import Blueprint, request, current_app
from utils.broadcast import broadcast


stake_bp = Blueprint("stake", __name__)


@stake_bp.route("/stake/set", methods=["POST"])
def set_stake():
    """NOTE
    request.json = {
        "stake_value": 100,  # integer
    }
    """

    my_state = current_app.config["my_state"]

    my_state.set_stake(request.json["stake_value"])

    # TODO: check that the new stake value is valid based on the remaining BCC of the recipient's wallet

    # TODO: set the change of the node's stake value

    # TODO: broadcast the new stake value of the node to the other nodes

    return True

@stake_bp.route("/stake/view", methods=["GET"])
def view_stake():
    pass
