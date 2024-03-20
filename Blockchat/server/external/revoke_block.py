from flask import Blueprint, request, current_app
from models.block import Block

revoke_block_bp = Blueprint("revokeBlock", __name__)


@revoke_block_bp.route("/revokeBlock", methods=["POST"])
def revoke_block():
    my_state = current_app.config["my_state"]
    block = Block.to_dict(request.json["block"])

    # TODO: procedure that revokes the block
    most_recent_block = my_state.blockchain.block_list[-1]
    if most_recent_block.current_hash == block.current_hash:
        my_state.blockchain.block_list[-1]

    response = {"status": "Block revoked"}
    status_code = 200

    return response, status_code
