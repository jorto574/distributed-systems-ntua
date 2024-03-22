from flask import Blueprint, request, current_app
from utils.broadcast import broadcast


set_stake_bp = Blueprint("set_stake", __name__)


@set_stake_bp.route("/set_stake", methods=["POST"])
def set_stake():
    """NOTE
    request.json = {
        "stake_value": 100,  # integer
        "recipient_id": 1,  # node of which the stake will change
    }
    """

    my_state = current_app.config["my_state"]

    new_stake_value = request.json["stake_value"]
    recipient_id = int(request.json(["recipient_id"]))

    # TODO: check that the new stake value is valid based on the remaining BCC of the recipient's wallet

    # TODO: set the change of the node's stake value

    # TODO: broadcast the new stake value of the node to the other nodes

    return True
