from flask import Flask, request, jsonify

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

@app.route('/receiveIpsPortsPksFromBootstrap', methods=['POST'])
def receive_ips_ports_pks_from_bootsrap():
    try:
        request_data = request.get_json()
        print(request_data)

        response_data = {
            "status": "success"
        }
        response = jsonify(response_data)

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
    app.run(debug=True, port=3001)