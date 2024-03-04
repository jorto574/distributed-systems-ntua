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


