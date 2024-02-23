class Block:
    """ current_index = 0 # index of the most recently added block
    current_hash = 1 # hash of the most recently added block
    capacity = 10 # maximum number of transactions in each block """

    def __init__(self, index, timestamp, transactions, validator, current_hash, previous_hash):
        self.index = index
        self.timestamp = timestamp # take current time stamp
        self.transactions = transactions
        self.validator = validator
        self.current_hash = current_hash
        self.previous_hash = previous_hash

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def to_dict(self):
        return {
            "block": {
                "index": self.index,
                "timestamp": self.timestamp,
                "transactions": [transaction.to_dict() for transaction in self.transactions],
                "validator": self.validator,
                "current_hash": self.current_hash,
                "previous_hash": self.previous_hash
            }
        }