import time
import requests

from models.block import Block
from models.blockchain import Blockchain
from models.transaction import Transaction
from models.wallet import PublicWallet, PrivateWallet
from models.state import State


def init_bootstrap(url, port, node_num, capacity):
    # Create a wallet for the bootsrap
    node_id = 0
    node_address = url + ":" + port
    my_wallet = PrivateWallet(node_id, node_address)
    amount = 1000 * node_num

    new_transaction = my_wallet.create_transaction(
        [0, 0], my_wallet.public_key, "coins", amount, "Genesis transaction", 0
    )

    # Initiate the blockchain
    my_blockchain = Blockchain([], capacity)

    # Create genesis_block
    index = 0
    timestamp = time.time()
    transactions = [new_transaction]
    validator = 0

    previous_hash = 1
    genesis_block = Block(index, timestamp, transactions, validator, previous_hash)
    print(f"genesis_block.current_hash = {genesis_block.current_hash}")

    # Add genesis block to the blockchain
    my_blockchain.add_block(genesis_block)

    # Create the State
    my_wallet_for_state = PublicWallet(
        node_id, node_address, my_wallet.public_key, amount
    )

    # TODO add a stake
    my_state = State(my_blockchain, [my_wallet_for_state], node_num, my_wallet)
    my_state.my_nonce += 1

    return my_state


def init_node(url, port, bootstrap):
    # Create a wallet for the node
    node_address = url + ":" + port

    my_wallet = PrivateWallet(None, node_address)

    # send a request to the bootsrap, giving him your public key and receive your unique node_id
    try:
        payload = {"address": node_address, "public_key": my_wallet.public_key}

        # send to bootstrap my public key
        response = requests.post(f"http://{bootstrap}/talkToBootstrap", json=payload)
        if response.status_code == 200:
            response_json = response.json()

            # receive from bootstrap my node id
            node_id = response_json.get("id")

            print(f"Request successful. Node ID: {node_id}")
            my_wallet.node_id = node_id

        else:
            print(f"Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")

    return my_wallet
