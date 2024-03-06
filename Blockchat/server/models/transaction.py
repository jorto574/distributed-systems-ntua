class Transaction:
    global_nonce = -1

    def __init__(
        self,
        sender_address: str,
        receiver_address: str,
        type_of_transaction: str,
        amount: int,
        message: str,
        signature,
    ):
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
            "signature": self.signature,
        }

    @classmethod
    def from_dict(cls, transaction_dict):
        return cls(
            transaction_dict["sender_address"],
            transaction_dict["receiver_address"],
            transaction_dict["type_of_transaction"],
            transaction_dict["amount"],
            transaction_dict["message"],
            transaction_dict["signature"],
        )
