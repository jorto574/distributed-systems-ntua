from block import Block
from blockchain import Blockchain
from transaction import Transaction
from my_wallet import MyWallet
from wallet import Wallet
from state import State
import time

def init_bootstrap():
    # Create a wallet for the bootsrap
    public_key = 0  # TODO must create keys based on RSA (or another cryptosystem)
    private_key = 0 # TODO must create keys based on RSA (or another cryptosystem)
    amount = 0
    my_wallet = MyWallet(public_key, private_key, amount)

    # Create initial bootstrap transcation
    sender_address = 0
    receiver_address = 0 # TODO receiver must be the wallet of bootsrap node
    type_of_transaction = "coins"
    amount = 5000
    message = ""
    signature = 0 # TODO must create thee sign_transaction func
    new_transaction = Transaction(sender_address, receiver_address, type_of_transaction, amount, message, signature)
    
    my_wallet.set_amount(amount)

    # Create genesis_block
    index = 0
    timestamp = time.time()
    transactions = [new_transaction]
    validator = 0
    current_hash = 0 # TODO must use a hash function eg SHA256
    previous_hash = 1
    new_block = Block(index, timestamp, transactions, validator, current_hash, previous_hash)

    # Initiate the blockchain
    my_blockchain = Blockchain([new_block])

    # Create the State
    my_wallet_for_state = Wallet(public_key, amount)
    my_state = State(my_blockchain, [my_wallet_for_state], [])

    return my_state
    