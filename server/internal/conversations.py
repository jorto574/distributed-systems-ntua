from flask import Blueprint, request, current_app, jsonify

conversations_bp = Blueprint("conversations", __name__)


@conversations_bp.route("/conversations", methods=["GET"])
def balance():
    conversations = current_app.config["my_state"].conversations

    response_data = {"conversations": conversations}
    response_status = 200

    return jsonify(response_data), response_status
