from models.wallet import Wallet
from models.blockchain import Blockchain


class State:
    def __init__(self, blockchain: Blockchain, wallets: list[Wallet], node_num: int):
        self.blockchain = blockchain
        self.wallets = wallets
        self.stakes = [0] * node_num
        self.current_fees = 0  # total fees corresponding to transactions of one block
        self.test = "state"

    def wallets_serialization(self):
        wallets_list = []
        for wallet in self.wallets:
            wallets_list.append(wallet.to_dict())
        return wallets_list

    def wallets_deserialization(wallets_list):
        wallets = []
        for wallet_data in wallets_list:
            wallets.append(Wallet(**wallet_data))
        return wallets

    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def add_block(self, block):
        self.blockchain.add_block(block)

    def add_node(self, node):
        self.nodes.append(node)

    def perform_transaction(self):
        pass

    def validate_transaction(self):
        pass
