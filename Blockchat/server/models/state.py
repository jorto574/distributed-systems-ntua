from models.wallet import Wallet
from models.blockchain import Blockchain


class State:
    def __init__(self, blockchain: Blockchain, wallets: list[Wallet], node_num: int):
        self.blockchain = blockchain
        self.wallets = wallets
        self.stakes = [0] * node_num
        self.current_fees = 0  # total fees corresponding to transactions of one block
        self.test = "state"

    def wallets_to_dict(self):
        wallets_dict = {}
        for address, wallet in self.wallets.items():
            wallets_dict[address] = wallet.to_dict()
        return wallets_dict

    def wallets_from_dict(wallets_dict):
        wallets = {}
        for address, wallet_data in wallets_dict.items():
            wallets[address] = Wallet(**wallet_data)
        return wallets

    def get_wallets(self):
        return self.wallets

    def add_wallet(self, address, wallet):
        self.wallets[address] = wallet

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
