from utils.crypto import generate_key_pairs, sign_message, verify_signature
from models.transaction import Transaction
from models.node import Node


class PrivateWallet:
    def __init__(self, node_id, node_address):
        self.node_id = node_id
        self.node_address = node_address
        self.public_key, self.private_key = generate_key_pairs()

    def create_transaction(
        self, sender_address, receiver_address, type_of_transaction, amount, message
    ):
        new_transaction = Transaction(
            sender_address, receiver_address, type_of_transaction, amount, message
        )

        def sign_transaction(transaction):
            message_to_sign = transaction.create_transaction_string()
            signature = sign_message(message_to_sign, self.private_key)
            return signature

        signature = sign_transaction(new_transaction)
        new_transaction.signature = signature
        return new_transaction

    # TODO validation includes checking if amount of sender is enough
    def validate_transaction(transaction):
        def verify_transaction_signature():
            return verify_signature(
                transaction.get_signature,
                transaction.get_sender_address(),
                transaction.create_transaction_string(),
            )

        return verify_transaction_signature()


class PublicWallet:
    def __init__(self, node_id, node_address, public_key, amount, stake=0):
        self.node_id = node_id
        self.node_address = node_address
        self.public_key = public_key
        self.amount = amount
        self.stake = stake

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "node_address": self.node_address,
            "public_key": self.public_key,
            "amount": self.amount,
            "stake": self.stake,
        }

    @classmethod
    def from_dict(cls, wallet_dict):
        return cls(
            wallet_dict["node_id"],
            wallet_dict["node_address"],
            wallet_dict["public_key"],
            wallet_dict["amount"],
            wallet_dict["stake"],
        )
