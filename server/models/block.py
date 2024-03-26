from hashlib import sha256
import time

from models.transaction import Transaction


class Block:
    def __init__(
        self,
        index,
        timestamp,
        transactions: list[Transaction],
        validator,
        previous_hash,
        current_hash=None,
    ):
        self.index = index
        self.timestamp = timestamp  # take current time stamp
        self.transactions = transactions
        self.validator = validator
        if current_hash:
            self.current_hash = current_hash
        else:
            self.current_hash = self.create_block_hash()
        self.previous_hash = previous_hash

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [
                transaction.to_dict() for transaction in self.transactions
            ],
            "validator": self.validator,
            "current_hash": self.current_hash,
            "previous_hash": self.previous_hash,
        }

    @classmethod
    def from_dict(cls, block_dict):
        return cls(
            block_dict["index"],
            block_dict["timestamp"],
            [Transaction.from_dict(t) for t in block_dict["transactions"]],
            block_dict["validator"],
            block_dict["previous_hash"],
            block_dict["current_hash"],
        )

    # Creates block hash for the new block the be validated and added to the blockchain
    def create_block_hash(self):
        transactions_string = ""
        for transaction in self.transactions:
            transactions_string += transaction.create_transaction_string()

        block_string = (
            str(self.index)
            + str(self.timestamp)
            + str(transactions_string)
            + str(self.validator)
        )

        sha256_hash_object = sha256()
        sha256_hash_object.update(block_string.encode("utf-8"))
        block_string_hashed = sha256_hash_object.hexdigest()

        return block_string_hashed
