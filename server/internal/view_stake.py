from flask import Blueprint, request, current_app

view_stake_bp = Blueprint("view_stake", __name__)


@view_stake_bp.route("/view_stake", methods=["POST"])
def view_stake():
    pass
