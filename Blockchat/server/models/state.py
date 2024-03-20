from models.wallet import Wallet
from models.blockchain import Blockchain
from models.transaction import Transaction
from models.my_wallet import MyWallet
from models.block import Block
from utils.broadcast import broadcast
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
        self.transaction_waiting_room = {}
        self.block_waiting_room = {}

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

        # if capacity is full, a new block must be created
        if len(self.blockchain.transaction_inbox) == self.blockchain.capacity:
            new_block_index = self.blockchain.block_list[-1].index + 1
            print(
                f"Block with index {new_block_index} has closed. Proof of stake begins"
            )
            seed = self.blockchain.block_list[-1].current_hash
            print(f"seed = {seed}")
            seed = int(("0x" + str(seed)), 16)
            validator_id = proof_of_stake(self.stakes, seed)
            print(f"Proof of stake ended with validator node_id {validator_id}")

            # if current node is validator, he mints the new block
            if validator_id == self.my_wallet.node_id:
                minted_block = self.mint_block()
                breakpoint()
                print(
                    f"Broadcasting block with index {minted_block.index} to all nodes"
                )
                # success is true if the validation of the block from every node is correct
                success = self.broadcast_block(minted_block)
                if success:
                    # add block to blockchain if everyone validated it
                    print(
                        f"Block block with index {minted_block.index} is validated from all nodes! Adding it to the blockchain"
                    )
                    self.add_block(minted_block)
                    self.update_transaction_inbox(minted_block)
                # if one or more nodes have rejected the block, revoke it
                else:
                    print(
                        f"Block block with index {minted_block.index} is rejected from some nodes! Revoking it..."
                    )
                    self.revoke_block(minted_block)

    def mint_block(self):
        transactions_list = list(self.blockchain.transaction_inbox.values())
        validator_public_key = self.my_wallet.public_key
        new_block = Block(
            self.blockchain.block_list[-1].index + 1,
            time.time(),
            transactions_list,
            validator_public_key,
            self.blockchain.create_block_hash(),
            self.blockchain.block_list[-1].current_hash,
        )
        return new_block

    def broadcast_block(self, block):
        broadcast(
            "/validateBlock",
            {"block": block.to_dict()},
            self.wallets,
            self.my_wallet.address,
        )

    def revoke_block(self, block):
        broadcast(
            "/revokeBlock",
            {"block": block.to_dict()},
            self.wallets,
            self.my_wallet.address,
        )

    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def add_block(self, block):
        self.blockchain.add_block(block)

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

        if not enough_amount:
            if verbose:
                print(
                    "Transaction validation failed: Not enough BCC to perform transaction"
                )
            return False

        # TODO: add transaction to waiting room

        return True

    def validate_block(self, block):
        incoming_validator_public_key = block.validator

        current_seed = self.blockchain.block_list[-1].current_hash
        current_seed = int(("0x" + str(current_seed)), 16)
        current_validator_id = proof_of_stake(self.stakes, current_seed)
        current_validator_public_key = self.wallets[current_validator_id].public_key

        is_correct_validator = (
            incoming_validator_public_key == current_validator_public_key
        )

        current_hash_of_previous_block = self.blockchain.block_list[-1].current_hash
        is_correct_current_hash_of_previous_block = (
            current_hash_of_previous_block == block.previous_hash
        )

        return is_correct_validator and is_correct_current_hash_of_previous_block

    def update_transaction_inbox(self, block):

        for transaction in block.transactions:
            sender_address = tuple(transaction.sender_address)
            nonce = transaction.nonce
            key = (sender_address, nonce)
            self.blockchain.blockchain_transactions[key] = transaction

        for transaction_key in self.blockchain.blockchain_transactions.keys():
            if transaction_key in self.blockchain.transaction_inbox:
                del self.blockchain.transaction_inbox[transaction_key]
                del self.blockchain.blockchain_transactions[transaction_key]
