from math import ceil


class Transaction:
    global_nonce = -1

    def __init__(
        self,
        sender_public_key: list[str],
        receiver_public_key: list[str],
        type: str,
        amount: int,
        message: str,
        nonce: int,
        signature=None,
        is_init: int = 0,
    ):
        self.nonce = nonce
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.type = type
        self.amount = amount
        self.message = message
        self.signature = signature
        self.is_init = is_init
        self.fees, self.total_amount = self.compute_fees()

    # Return the concatenation of every field of a transaction
    def create_transaction_string(self):
        str_nonce = str(self.nonce)
        str_sender_public_key = str(self.sender_public_key[0]) + str(
            self.sender_public_key[1]
        )
        if self.type == "stake":
            str_receiver_public_key = str(self.receiver_public_key)
        else:
            str_receiver_public_key = str(self.receiver_public_key[0]) + str(
                self.receiver_public_key[1]
            )
        str_type_of_transaction = str(self.type)
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
            "type": self.type,
            "amount": self.amount,
            "message": self.message,
            "signature": self.signature,
            "is_init": self.is_init,
        }

    @classmethod
    def from_dict(cls, transaction_dict):
        return cls(
            transaction_dict["sender_public_key"],
            transaction_dict["receiver_public_key"],
            transaction_dict["type"],
            transaction_dict["amount"],
            transaction_dict["message"],
            transaction_dict["nonce"],
            transaction_dict["signature"],
            transaction_dict["is_init"],
        )

    def compute_fees(self):
        if self.is_init == 1:  # Initial transactions from bootstrap
            fees = 0
            total_amount = 0
        elif self.type == "coins":
            fees = (0.3) * self.amount
            total_amount = ceil(self.amount + fees)
        elif self.type == "message":
            fees = len(self.message)
            total_amount = fees
        elif self.type == "stake":
            fees = 0
            total_amount = self.amount

        return fees, total_amount
