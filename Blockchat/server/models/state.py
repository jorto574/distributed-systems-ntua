from models.my_wallet import MyWallet

class State:
    def __init__(self, blockchain, wallets):
        self.blockchain = blockchain
        self.wallets = wallets
        self.stakes = []
        self.current_fees = 0 # total fees corresponding to transactions of one block
        self.test = "state"

    def wallets_to_dict(self):
        wallets_dicts = {}
        for address, wallet in self.wallets.items():
            wallets_dicts[address] = wallet.to_dict()

    def wallets_from_dict(cls, wallets_dict):
        wallets = {}
        for address, wallet_data in wallets_dict.items():
            wallets[address] = MyWallet(**wallet_data)
        return wallets


    def get_wallets(self):
        return self.wallets
    
    def add_wallet(self, address, wallet):
        self.wallets[address]= wallet

    def add_block(self, block):
        self.blockchain.add_block(block)

    def add_node(self, node):
        self.nodes.append(node)

    def get_blockchain(self):
        return self.blockchain
    
    def get_nodes(self):
        return self.nodes

    def perform_transaction(self):
        pass

    def validate_transaction(self):
        pass
