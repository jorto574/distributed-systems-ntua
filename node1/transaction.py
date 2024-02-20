from wallet import Wallet
from state import State

class Transaction:
    global_nonce = 0

    def __init__(self, sender_address, receiver_address, type_, amount, message, nonce, signature):
        Transaction.global_nonce += 1

        self.nonce = Transaction.global_nonce
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.type_of_transaction = type_
        self.amount = amount
        self.message = message
        self.nonce = nonce
        self.signature = signature

    def broadcast_transaction(self):
        # TODO somehow collect all public keys 
        public_keys = [Wallet.get_public_key() for Wallet in State.get_wallets()]

        # TODO after collecting all pks, send an http request to all nodes 
    
