class State:
    def __init__(self, blockchain, wallets, stakes, nodes):
        self.blockchain = blockchain
        self.wallets = wallets
        self.stakes = stakes
        self.nodes = nodes
        self.current_fees = 0 # total fees corresponding to transactions of one block

    def get_wallets(self):
        return self.wallets
    
    def add_wallet(self, wallet):
        self.wallets.append(wallet)

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

    def print_state(self):
        print("state")
