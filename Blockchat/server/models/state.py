from models.wallet import Wallet
from models.blockchain import Blockchain
from models.transaction import Transaction
from models.my_wallet import MyWallet
from models.block import Block
from utils.proof_of_stake import proof_of_stake
from utils.crypto import verify_signature
import time
from math import ceil


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
        self.fees = 0

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

        # # if capacity is full, a new block must be created
        # if len(self.blockchain.transaction_inbox) == self.blockchain.capacity:
        #     seed = self.blockchain.block_list[-1].current_hash
        #     seed = int(seed, 16)
        #     validator_id = proof_of_stake(self.stakes, seed)

        #     # if current node is validator, he mints the new block
        #     if validator_id == self.my_wallet.node_id:
        #         minted_block = self.mint_block()
        #         success = self.broadcast_block(minted_block)
        #         if success:
        #             # add block to blockchain if everyone validated it
        #             self.add_block(minted_block)

    def mint_block(self):
        transactions_list = list(self.blockchain.transaction_inbox.values())
        validator_public_key = self.my_wallet.public_key
        new_block = Block(
            # TODO, must fix index
            1,
            time.time(),
            transactions_list,
            validator_public_key,
            self.blockchain.create_block_hash(),
            self.blockchain.block_list[-1].current_hash,
        )
        return new_block

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

    # TODO this is temporary solution. This must change to a dictionary of node ids with public keys
    def find_wallet_from_public_key(self, public_key):
        for wallet in self.wallets:
            if public_key == wallet.public_key:
                return wallet

    def validate_transaction(self, transaction, verbose=False):
        signature_verified = verify_signature(
            transaction.signature,
            transaction.sender_address,
            transaction.create_transaction_string(),
        )
        if not signature_verified:
            if verbose:
                print("Transaction validation failed: error verifying the signature")
            return False

        # must find the sender wallet amount
        sender_public_key = transaction.sender_address
        sender_wallet = self.find_wallet_from_public_key(sender_public_key)

        receiver_public_key = transaction.receiver_address
        receiver_wallet = self.find_wallet_from_public_key(receiver_public_key)
        breakpoint()
        enough_amount = False
        if transaction.amount >= 0:
            fees = (0.3) * transaction.amount
            total_amount = ceil(transaction.amount + fees)

        if transaction.message != "":
            fees = len(transaction.message)
            total_amount = fees

        if total_amount > sender_wallet.amount:
            enough_amount = False
        else:
            enough_amount = True
            self.fees += fees

        if not enough_amount:
            if verbose:
                print(
                    "Transaction validation failed: Not enough BCC to perform transaction"
                )
            return False

        sender_wallet.amount -= total_amount
        receiver_wallet.amount += total_amount
        return True
