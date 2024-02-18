class block:

    current_index = 0 # index of the most recently added block
    current_hash = 1 # hash of the most recently added block
    capacity = 10 # maximum number of transactions in each block

    def __init__(self, transactions, previous_hash, validator):
        self.index = current_index

        self.time_stamp = 0 # take current time stamp

        self.transactions = transactions

        self.previous_hash = current_hash
