class Transaction:
    global_nonce = -1

    def __init__(
        self,
        sender_public_key: list[str],
        receiver_public_key: list[str],
        type_of_transaction: str,
        amount: int,
        message: str,
        nonce: int,
        signature=None,
    ):
        self.nonce = nonce
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.type_of_transaction = type_of_transaction
        self.amount = amount
        self.message = message
        self.signature = signature

    # Return the concatenation of every field of a transaction
    def create_transaction_string(self):
        str_nonce = str(self.nonce)
        str_sender_public_key = str(self.sender_public_key[0]) + str(
            self.sender_public_key[1]
        )
        str_receiver_public_key = str(self.receiver_public_key[0]) + str(
            self.receiver_public_key[1]
        )
        str_type_of_transaction = str(self.type_of_transaction)
        str_amount = str(self.amount)
        str_message = str(self.message)

        message_to_hash = (
            str_nonce
            + str_sender_public_key
            + str_receiver_public_key
            + str_type_of_transaction
            + str_amount
            + str_message
        )

        return message_to_hash

    def to_dict(self):
        return {
            "nonce": self.nonce,
            "sender_public_key": self.sender_public_key,
            "receiver_public_key": self.receiver_public_key,
            "type_of_transaction": self.type_of_transaction,
            "amount": self.amount,
            "message": self.message,
            "signature": self.signature,
        }

    @classmethod
    def from_dict(cls, transaction_dict):
        return cls(
            transaction_dict["sender_public_key"],
            transaction_dict["receiver_public_key"],
            transaction_dict["type_of_transaction"],
            transaction_dict["amount"],
            transaction_dict["message"],
            transaction_dict["nonce"],
            transaction_dict["signature"],
        )
