from flask import Blueprint

state_bp = Blueprint("state", __name__)


@state_bp.route("/", methods=["GET"])
def state():
    global my_state
    return my_state.test
