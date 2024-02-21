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

