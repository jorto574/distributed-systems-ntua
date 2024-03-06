class Transaction:
    global_nonce = -1

    def __init__(
        self,
        sender_address: list[str],
        receiver_address: list[str],
        type_of_transaction: str,
        amount: int,
        message: str,
    ):
        Transaction.global_nonce += 1

        self.nonce = Transaction.global_nonce
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.type_of_transaction = type_of_transaction
        self.amount = amount
        self.message = message
        self.signature = None

    # Return the hashed concatenation of every field of a transaction
    def create_transaction_string(self):
        str_nonce = str(self.nonce)
        str_sender_address = str(self.sender_address[0]) + str(self.sender_address[1])
        str_receiver_address = str(self.receiver_address[0]) + str(
            self.receiver_address[1]
        )
        str_type_of_transaction = str(self.type_of_transaction)
        str_amount = str(self.amount)
        str_message = str(self.message)

        message_to_hash = (
            str_nonce
            + str_sender_address
            + str_receiver_address
            + str_type_of_transaction
            + str_amount
            + str_message
        )

        return message_to_hash

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
