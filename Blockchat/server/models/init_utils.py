import time
import requests

from models.block import Block
from models.blockchain import Blockchain
from models.transaction import Transaction
from models.my_wallet import MyWallet
from models.wallet import Wallet
from models.state import State
from models.node import Node

def init_bootstrap(url,port,node_num):
    # Create a wallet for the bootsrap
    public_key = 0  # TODO must create keys based on RSA (or another cryptosystem)
    private_key = 0 # TODO must create keys based on RSA (or another cryptosystem)
    amount = 0
    node_id = 0
    address = url + ":" + port
    my_wallet = MyWallet(node_id, address, public_key, private_key)

    # Create initial bootstrap transcation
    sender_address = address
    receiver_address = address
    type_of_transaction = "coins"
    amount = 1000*node_num
    message = ""
    signature = 0 # TODO must create thee sign_transaction func
    new_transaction = Transaction(sender_address, receiver_address, type_of_transaction, amount, message, signature)

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
    my_wallet_for_state = Wallet(node_id,address, public_key, amount)

    # TODO add a stake
    my_state = State(my_blockchain, {address:my_wallet_for_state})

    return my_state, my_wallet

def init_node(url,port,bootstrap):
    # Create a wallet for the bootsrap
    public_key = 1  # TODO must create keys based on RSA (or another cryptosystem)
    private_key = 1 # TODO must create keys based on RSA (or another cryptosystem)
    amount = 0
    address = url + ":" + port
    
    # send a request to the bootsrap, giving him your public key and receive your unique node_id
    try:
        payload = {
            "address": address,
            "public_key": public_key
        }

        # send to bootstrap my public key
        response = requests.post(f"http://{bootstrap}/talkToBootstrap", json = payload)
        if response.status_code == 200:
            response_json = response.json()

            # receive from bootstrap my node id
            node_id = response_json.get("id")

            if node_id is not None:
                print(f"Request successful. Node ID: {node_id}")
            else:
                print("Node ID not found in the response.")
        else:
            print(f"Request failed with status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
    
    my_wallet = MyWallet(node_id, address, public_key, private_key)

    return my_wallet
