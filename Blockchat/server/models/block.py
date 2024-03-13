from models.transaction import Transaction


class Block:
    def __init__(
        self,
        index,
        timestamp,
        transactions: list[Transaction],
        validator,
        current_hash,
        previous_hash,
    ):
        self.index = index
        self.timestamp = timestamp  # take current time stamp
        self.transactions = transactions
        self.validator = validator
        self.current_hash = current_hash
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
            block_dict["current_hash"],
            block_dict["previous_hash"],
        )
