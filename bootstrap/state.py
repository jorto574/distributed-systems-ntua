class State:
    def __init__(self, blockchain, wallets, stakes):
        self.blockchain = blockchain
        self.wallets = wallets
        self.stakes = stakes
        self.current_fees = 0 # total fees corresponding to transactions of one block

    def get_wallets(self):
        return self.wallets
    
    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def perform_transaction(self):
        pass

    def validate_transaction(self):
        pass
