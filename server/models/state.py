from models.wallet import PublicWallet, PrivateWallet
from models.blockchain import Blockchain
from models.block import Block
from utils.broadcast import broadcast
from utils.proof_of_stake import proof_of_stake
from utils.crypto import verify_signature
from utils.send_http_request import send_http_request
import time
import threading


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
        self.conversations = {i: [] for i in range(node_num)}

        self.public_key_to_node_id = {
            tuple(wallet.public_key): wallet.node_id for wallet in wallets
        }
        self.my_nonce = 0
        self.block_waiting_room = {}

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
            wallets.append(PublicWallet.from_dict(wallet_data))
        return wallets

    def validate_transaction(self, transaction, verbose=False, check_signature=True):

        transaction_key = self.transaction_unique_id(transaction)
        sender_public_key = transaction.sender_public_key
        sender_wallet = self.find_wallet_from_public_key(sender_public_key)

        if check_signature:
            signature_verified = verify_signature(
                transaction.signature,
                transaction.sender_public_key,
                transaction.create_transaction_string(),
            )
            if not signature_verified:
                if verbose:
                    print(
                        f"Validation of transaction {transaction_key} of type {transaction.type} failed:"
                        "error verifying the signature"
                    )
                return False

        enough_amount = False

        total_amount = transaction.total_amount

        if transaction.type == "stake":
            enough_amount = (
                sender_wallet.soft_amount + sender_wallet.stake
            ) > total_amount
        else:
            if total_amount > sender_wallet.soft_amount:
                enough_amount = False
            else:
                enough_amount = True

        if not enough_amount:
            if verbose:
                print(
                    f"Validation of transaction {transaction_key} of type {transaction.type} failed:"
                    "Not enough BCC to perform transaction"
                )
            return False

        # Transaction is valid
        self.blockchain.transaction_inbox[transaction_key] = transaction

        fees = transaction.fees
        total_amount = transaction.total_amount

        if transaction.type == "stake":
            sender_wallet.soft_amount += sender_wallet.stake - total_amount
            sender_wallet.stake = total_amount
        else:
            sender_wallet.soft_amount -= total_amount

        if transaction.type != "stake":  # coins and message transactions
            receiver_public_key = transaction.receiver_public_key
            receiver_wallet = self.find_wallet_from_public_key(receiver_public_key)
            receiver_wallet.soft_amount += total_amount - fees

        threading.Thread(target=self.block_val_process, args=()).start()

        return True

    # def add_transaction(self, transaction_key, is_init=False):
    #     sender_wallet = self.find_wallet_from_public_key(transaction.sender_public_key)

    #     if not is_init:

    #         if receiver_wallet.node_id == self.my_wallet.node_id:
    #             type = transaction.type
    #             print(f"You've received a transaction of type {type}")
    #             if type == "message":
    #                 self.conversations[transaction_key[0]].append(
    #                     [
    #                         "node_"
    #                         + str(transaction_key[0])
    #                         + "_"
    #                         + str(transaction_key[1]),
    #                         transaction.message,
    #                     ]
    #                 )

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
                    self.add_block(minted_block)
                    self.update_state(minted_block)
                    print(
                        f"Block with index {minted_block.index} succesfully broadcasted to all nodes"
                    )
                else:
                    print(f"Broadcast of block with index {minted_block.index} failed")

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

    # def broadcast_add_block(self, index):
    #     broadcast(
    #         "/addBlock",
    #         {"index": index},
    #         self.wallets,
    #         self.my_wallet.node_address,
    #     )

    def add_wallet(self, wallet):
        self.wallets.append(wallet)
        self.public_key_to_node_id[tuple(wallet.public_key)] = wallet.node_id

    def add_block(self, block):
        self.blockchain.add_block(block)

    def find_wallet_from_public_key(self, public_key):
        wallet = self.wallets[self.public_key_to_node_id[tuple(public_key)]]
        return wallet

    def validate_block(self, block):
        incoming_validator_public_key = block.validator
        incoming_validator_id = self.find_wallet_from_public_key(
            incoming_validator_public_key
        ).node_id

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

        if is_correct_validator and is_correct_current_hash_of_previous_block:
            print(f"Validated block with index {block.index}. Adding to blockchain")
            self.add_block(block)
            self.update_state(block)
            return True
        else:
            print(
                f"Failed to validate block with index {block.index} from node {incoming_validator_id}"
            )
            return False

    def transaction_unique_id(self, transaction):
        sender_public_key = tuple(transaction.sender_public_key)
        node_id = self.public_key_to_node_id[tuple(sender_public_key)]
        nonce = transaction.nonce
        key = (node_id, nonce)
        return key

    def update_state(self, block):
        validator_id = self.public_key_to_node_id[tuple(block.validator)]

        # update hard amounts based on the transactions in the new block
        for transaction in block.transactions:
            if transaction.is_init == 0:
                key = self.transaction_unique_id(transaction)

                sender_public_key = transaction.sender_public_key
                sender_wallet = self.find_wallet_from_public_key(sender_public_key)

                total_amount = transaction.total_amount

                if transaction.type == "stake":
                    sender_id = sender_wallet.node_id
                    old_stake = self.stakes[sender_id]
                    sender_wallet.hard_amount += old_stake - total_amount
                    self.stakes[sender_id] = total_amount
                    sender_wallet.stake = total_amount
                else:  # for coins and message transactions
                    sender_wallet.hard_amount -= total_amount
                    fees = transaction.fees
                    self.wallets[validator_id].hard_amount += fees
                    receiver_public_key = transaction.receiver_public_key
                    receiver_wallet = self.find_wallet_from_public_key(
                        receiver_public_key
                    )
                    receiver_wallet.hard_amount += total_amount - fees

                if key in self.blockchain.transaction_inbox:
                    del self.blockchain.transaction_inbox[key]
                else:
                    self.blockchain.blockchain_transactions[key] = transaction
        print(self.stakes)
        print(self.blockchain.transaction_inbox)
        # update soft amounts to much the updated hard amounts
        for wallet in self.wallets:
            wallet.soft_amount = wallet.hard_amount
        # re-validate the remaining transactions
        remaining_transactions = list(self.blockchain.transaction_inbox.values())
        self.blockchain.transaction_inbox = {}
        for transaction in remaining_transactions:
            if transaction.is_init != 1:
                self.validate_transaction(transaction, check_signature=False)

    # def set_stake(self, stake_amount):
    #     # NOTE: the recipient id of the transaction that is created by set_stake() will be -1 due to the fact that
    #     #       the node ids start from 0.
    #     payload = {"recipient_id": -1, "type": "stake", "body": stake_amount}

    #     send_http_request("POST", self.my_wallet.address, "send_transaction", payload)
