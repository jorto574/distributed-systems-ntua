from utils.crypto import generate_key_pairs, sign_message, verify_signature
from transaction import Transaction


class MyWallet:
    def __init__(self, node_id, address):
        self.node_id = node_id
        self.public_key, self.private_key = generate_key_pairs()
        self.address = address

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
