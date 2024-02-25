from block import Block
from blockchain import Blockchain
from transaction import Transaction
from my_wallet import MyWallet
from wallet import Wallet, my_wallet
from state import State
from node import Node
import time

def init_bootstrap():
    # Create a wallet for the bootsrap
    # amount = 0
    # my_wallet = MyWallet(amount)
   
    # Create a node for the bootstrap
    my_node = Node(0, "127.0.0.1", 3000, my_wallet.get_public_key())

    # Create initial bootstrap transcation
    sender_address = 0
    receiver_address = my_wallet.get_puvlic_key()
    type_of_transaction = "coins"
    amount = 5000
    message = ""
    signature = 0 # TODO must create thee sign_transaction func
    new_transaction = my_wallet.create_transaction(sender_address, receiver_address, type_of_transaction, amount, message, signature)
    
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
    my_wallet_for_state = Wallet(my_wallet.get_public_key(), amount)

    # TODO add a stake
    my_state = State(my_blockchain, [my_wallet_for_state], [], [my_node])

    return my_state
    