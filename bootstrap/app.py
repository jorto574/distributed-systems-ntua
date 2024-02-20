from flask import Flask, request, jsonify
from wallet import Wallet

app = Flask(__name__)

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

# when a node enters, it must send a request to this url
@app.route('/getBootstrapPublicKey')
def get_bootsrap_public_key():
    public_key = Wallet.get_public_key()
    response_data = {
        "status": "success",
        "public_key": public_key
    }
    response = jsonify(response_data)
    return response, 200
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)