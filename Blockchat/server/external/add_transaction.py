from flask import Blueprint, request, current_app
from models.transaction

add_transaction_bp = Blueprint("add_transaction", __name__)


@add_transaction_bp.route("/addTransaction", methods=["POST"])
def revoke_block():
    my_state = current_app.config["my_state"]
    data = request.json
    transaction = Transaction.from_dict(data["transaction"])

    self.fees += fees
    sender_wallet.amount -= total_amount
    receiver_wallet.amount += total_amount

    most_recent_block = my_state.blockchain.block_list[-1]
    if most_recent_block.current_hash == block.current_hash:
        my_state.blockchain.block_list[-1]

    response = {"status": "Block revoked"}
    status_code = 200

    return response, status_code
