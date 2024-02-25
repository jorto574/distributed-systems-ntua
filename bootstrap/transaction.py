from my_wallet import MyWallet
from state import State
from crypto import sha256_hash

class Transaction:
    global_nonce = -1

    def __init__(self, sender_address, receiver_address, type_of_transaction, amount, message, signature):
        Transaction.global_nonce += 1

        self.nonce = Transaction.global_nonce
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.type_of_transaction = type_of_transaction
        self.amount = amount
        self.message = message
        self.signature = signature

    def get_signature(self):
        return self.signature
    
    def get_sender_address(self):
        return self.sender_address

    # Return the hashed concatenation of every field of a transaction
    def create_transaction_string(self):
        str_nonce = str(self.nonce)
        str_sender_address = str(self.sender_address)
        str_receiver_address = str(self.receiver_address)
        str_type_of_transaction = str(self.type_of_transaction)
        str_amount = str(self.amount)
        str_message = str(self.message)

        message_to_hash = str_nonce + str_sender_address + str_receiver_address + str_type_of_transaction + str_amount + str_message

        return message_to_hash
    
    def to_dict(self):
        return {
            "nonce": self.nonce,
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "type_of_transaction": self.type_of_transaction,
            "amount": self.amount,
            "message": self.message,
            "signature": self.signature
        }

    
