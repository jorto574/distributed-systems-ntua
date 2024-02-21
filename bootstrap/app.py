from flask import Flask, request, jsonify
from dotenv import load_dotenv, dotenv_values
from my_wallet import MyWallet
from wallet import Wallet
from state import State
from init_bootstrap import init_bootstrap
import os

app = Flask(__name__)
load_dotenv()

BASE_URL = os.environ.get("BASE_URL")
PORT = os.environ.get("PORT")
print(PORT)

@app.route('/')
def hello_world():
    return 'Hello, World! This is a Flask server.'


@app.route('/validateTransaction', methods=['POST'])
def validate_transaction():
    if not request.is_json:
        return jsonify({"error": "Invalid request, must provide JSON data"}), 400
    
    transaction_data = request.get_json()
    transaction = transaction_data['transaction']

    return

@app.route('/validateBlock', methods=['POST'])
def validate_block():
    if not request.is_json:
        return jsonify({"error": "Invalid request, must provide JSON data"}), 400
    
    block_data = request.get_json()
    block = block_data['block']

    return


@app.route('/receiveMessage')
def receive_message():
    transaction_kind = request.args.get('transaction_kind', '')
    return

node_id = 0
# when a node enters, it must send a request to this url
@app.route('/talkToBootstrap', methods=['GET', 'POST'])
def talk_to_bootstrap():
    global my_state
    try:
        print("got to the request!")
        global node_id
        node_id += 1

        request_data = request.get_json()
        node_public_key = request_data.get("public_key")
        print(node_public_key)
        node_wallet = Wallet(node_public_key, 0)
        my_state.add_wallet(node_wallet)

        response_data = {
            "status": "success",
            "id": node_id
        }
        response = jsonify(response_data)
        print(response)
        return response, 200
    
    except Exception as e:
        print(f"An error occurred: {e}")
        response_data = {
            "status": "failed",
            "error": str(e)  
        }
        response = jsonify(response_data)
        return response, 500


if __name__ == '__main__':
    my_state = init_bootstrap()
    app.run(debug=True, port=3000)