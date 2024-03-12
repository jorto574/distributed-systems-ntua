from models.wallet import Wallet
from models.blockchain import Blockchain
from models.transaction import Transaction
from models.my_wallet import MyWallet
from utils.proof_of_stake import proof_of_stake


class State:
    def __init__(
        self,
        blockchain: Blockchain,
        wallets: list[Wallet],
        node_num: int,
        my_wallet: MyWallet,
    ):
        self.blockchain = blockchain
        self.wallets = wallets
        self.stakes = [0] * node_num
        self.current_fees = 0  # total fees corresponding to transactions of one block
        self.test = "state"
        self.my_wallet = my_wallet

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

    def add_transaction(self, transaction: Transaction):
        sender_address = tuple(transaction.sender_address)
        nonce = transaction.nonce
        key = (sender_address, nonce)
        self.blockchain.transaction_inbox[key] = transaction
        if len(self.blockchain.transaction_inbox) == self.blockchain.capacity:
            validator_id = proof_of_stake(self.stakes)
            if validator_id == self.my_wallet.node_id:
                minted_block = self.mint_block()
                success = self.broadcast_block(minted_block)
                if success:
                    self.add_block(minted_block)

    def mint_block(self):
        # TODO
        pass

    def broadcast_block(self):
        # TODO
        pass

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
