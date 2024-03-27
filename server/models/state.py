from models.wallet import PublicWallet, PrivateWallet
from models.blockchain import Blockchain
from models.transaction import Transaction
from models.block import Block
from utils.broadcast import broadcast
from utils.proof_of_stake import proof_of_stake
from utils.crypto import verify_signature
from utils.send_http_request import send_http_request
import time
import threading
from collections import OrderedDict


class State:
    def __init__(
        self,
        blockchain: Blockchain,
        wallets: list[PublicWallet],
        node_num: int,
        my_wallet: PrivateWallet,
    ):
        self.blockchain = blockchain
        self.wallets = wallets
        self.stakes = [0] * node_num
        self.current_fees = 0  # total fees corresponding to transactions of one block
        self.test = "state"
        self.my_wallet = my_wallet

        # Waiting rooms for 2PC implementation: validated transactions/blocks watining the OK from the coordinator.
        # In block_waiting_room coordinator is the validator in transaction_waiting_room coordinator is the sender.
        self.block_waiting_room = {}
        self.transaction_waiting_room = {}

        self.conversations = {i: [] for i in range(node_num)}

        self.public_key_to_node_id = {
            tuple(wallet.public_key): wallet.node_id for wallet in wallets
        }
        self.my_nonce = 0

    def get_my_nonce(self):
        nonce = self.my_nonce
        self.my_nonce += 1
        return nonce

    def wallets_serialization(self):
        wallets_list = []
        for wallet in self.wallets:
            wallets_list.append(wallet.to_dict())
        return wallets_list

    def wallets_deserialization(wallets_list):
        wallets = []
        for wallet_data in wallets_list:
            wallets.append(PublicWallet(**wallet_data))
        return wallets

    def add_transaction(self, transaction_key, is_init=False):
        transaction = self.transaction_waiting_room[transaction_key]
        self.blockchain.transaction_inbox[transaction_key] = transaction
        del self.transaction_waiting_room[transaction_key]
        sender_wallet = self.find_wallet_from_public_key(transaction.sender_public_key)
        receiver_wallet = self.find_wallet_from_public_key(
            transaction.receiver_public_key
        )
        if not is_init:
            fees = transaction.fees
            total_amount = transaction.total_amount
            # self.fees += fees
            sender_wallet.amount -= total_amount
            receiver_wallet.amount += total_amount - fees

            if receiver_wallet.node_id == self.my_wallet.node_id:
                type = transaction.type_of_transaction
                print(f"You've received a transaction of type {type}")
                if type == "message":
                    self.conversations[transaction_key[0]].append(
                        [
                            "node_"
                            + str(transaction_key[0])
                            + "_"
                            + str(transaction_key[1]),
                            transaction.message,
                        ]
                    )

            threading.Thread(target=self.block_val_process, args=()).start()

    def block_val_process(self):
        # if capacity is full, a new block must be created
        if len(self.blockchain.transaction_inbox) == self.blockchain.capacity:
            new_block_index = self.blockchain.block_list[-1].index + 1
            print(
                f"Block with index {new_block_index} has closed. Proof of stake begins"
            )
            seed = self.blockchain.block_list[-1].current_hash

            seed = int(("0x" + str(seed)), 16)
            validator_id = proof_of_stake(self.stakes, seed)
            print(f"Proof of stake ended with validator node_id {validator_id}")

            # if current node is validator, he mints the new block
            if validator_id == self.my_wallet.node_id:
                minted_block = self.mint_block()
                print(
                    f"Broadcasting block with index {minted_block.index} to all nodes"
                )
                # success is true if the validation of the block from every node is correct
                success = self.broadcast_block(minted_block)
                if success:
                    # if every node has validated the block, broadcast to all nodes that they must add the block to their blockchain
                    self.broadcast_add_block(minted_block.index)

                    print(
                        f"Block block with index {minted_block.index} is validated from all nodes! Adding it to the blockchain"
                    )

                    # the validator aslo adds the block
                    self.add_block(minted_block)
                    self.update_transaction_inbox(minted_block)

    def mint_block(self):
        transactions_list = list(self.blockchain.transaction_inbox.values())
        validator_public_key = self.my_wallet.public_key
        new_block = Block(
            self.blockchain.block_list[-1].index + 1,
            time.time(),
            transactions_list,
            validator_public_key,
            self.blockchain.block_list[-1].current_hash,
        )
        return new_block

    def broadcast_block(self, block):
        return broadcast(
            "/validateBlock",
            {"block": block.to_dict()},
            self.wallets,
            self.my_wallet.node_address,
        )

    def broadcast_add_block(self, index):
        broadcast(
            "/addBlock",
            {"index": index},
            self.wallets,
            self.my_wallet.node_address,
        )

    def add_wallet(self, wallet):
        self.wallets.append(wallet)
        self.public_key_to_node_id[tuple(wallet.public_key)] = wallet.node_id

    def add_block(self, block):
        self.blockchain.add_block(block)

    def find_wallet_from_public_key(self, public_key):
        wallet = self.wallets[self.public_key_to_node_id[tuple(public_key)]]
        return wallet

    def validate_transaction(self, transaction, verbose=False):
        signature_verified = verify_signature(
            transaction.signature,
            transaction.sender_public_key,
            transaction.create_transaction_string(),
        )
        if not signature_verified:
            if verbose:
                print("Transaction validation failed: error verifying the signature")
            return False

        # must find the sender wallet amount
        sender_public_key = transaction.sender_public_key
        sender_wallet = self.find_wallet_from_public_key(sender_public_key)

        enough_amount = False
        
        total_amount = transaction.total_amount

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

        # TODO: add transaction to waiting room after it is validated correct
        self.transaction_waiting_room[self.transaction_unique_id(transaction)] = (
            transaction
        )
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

    def transaction_unique_id(self, transaction):
        sender_public_key = tuple(transaction.sender_public_key)
        node_id = self.public_key_to_node_id[tuple(sender_public_key)]
        nonce = transaction.nonce
        key = (node_id, nonce)
        return key

    def update_transaction_inbox(self, block):
        validator_id = self.public_key_to_node_id[tuple(block.validator)]
        for transaction in block.transactions:
            key = self.transaction_unique_id(transaction)
            fees = transaction.fees
            self.wallets[validator_id].amount += fees

            if key in self.blockchain.transaction_inbox:
                del self.blockchain.transaction_inbox[key]
            else:
                self.blockchain.blockchain_transactions[key] = transaction

    def set_stake(self, stake_amount):
        # NOTE: the recipient id of the transaction that is created by set_stake() will be -1 due to the fact that
        #       the node ids start from 0.
        payload = {"recipient_id": -1, "type": "coins", "body": stake_amount}

        send_http_request("POST", self.my_wallet.address, "send_transaction", payload)
