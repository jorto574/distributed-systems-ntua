import time
import requests

from models.block import Block
from models.blockchain import Blockchain
from models.transaction import Transaction
from models.my_wallet import MyWallet
from models.wallet import Wallet
from models.state import State
from models.node import Node

def init_bootstrap():
    # Create a wallet for the bootsrap
    public_key = 0  # TODO must create keys based on RSA (or another cryptosystem)
    private_key = 0 # TODO must create keys based on RSA (or another cryptosystem)
    amount = 0
    my_wallet = MyWallet(public_key, private_key, amount)

    # Create a node for the bootstrap
    my_node = Node(0, "127.0.0.1", 3000, public_key)

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

    # TODO add a stake
    my_state = State(my_blockchain, [my_wallet_for_state], [], [my_node])

    return my_state

def init_node():
    # Create a wallet for the bootsrap
    public_key = 1  # TODO must create keys based on RSA (or another cryptosystem)
    private_key = 1 # TODO must create keys based on RSA (or another cryptosystem)
    amount = 0
    my_wallet = MyWallet(public_key, private_key, amount)

    # send a request to the bootsrap, giving him your public key and receive your unique node_id
    def receive_id_from_bootstrap():
        url = "http://127.0.0.1"
        port = 3000
        public_key = my_wallet.get_public_key()
        try:
            payload = {
                "public_key": public_key
            }

            # send to bootstrap my public key
            response = requests.post(f"{url}:{port}/talkToBootstrap", json = payload)
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

    receive_id_from_bootstrap()