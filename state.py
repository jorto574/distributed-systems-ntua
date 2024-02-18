class state:
    def __init__(self, blockchain, wallets, stakes):
        self.blockchain = blockchain
        self.wallets = wallets
        self.stakes = stakes
        self.current_fees = 0 # total fees corresponding to transactions of one block

    def perform_transaction(self):
        pass

    def validate_transaction(self):
        pass
