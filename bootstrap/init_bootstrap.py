from block import Block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet
import time

def init_bootstrap():
    # Create a wallet for the bootsrap
    public_key = 0  # TODO must create keys based on RSA (or another cryptosystem)
    private_key = 0 # TODO must create keys based on RSA (or another cryptosystem)
    amount = 0
    new_wallet = Wallet(public_key, private_key, amount)

    # Create initial bootstrap transcation
    sender_address = 0
    receiver_address = 0 # TODO receiver must be the wallet of bootsrap node
    type_of_transaction = "coins"
    amount = 5000
    message = ""
    signature = 0 # TODO must create thee sign_transaction func
    new_transaction = Transaction(sender_address, receiver_address, type_of_transaction, amount, message, signature)
    
    new_wallet.set_amount(amount)

    # Create genesis_block
    index = 0
    timestamp = time.time()
    transactions = [new_transaction]
    validator = 0
    current_hash = 0 # TODO must use a hash function eg SHA256
    previous_hash = 1
    new_block = Block(index, timestamp, transactions, validator, current_hash, previous_hash)

    # Initiate the blockchain
    blockchain = Blockchain([new_block])