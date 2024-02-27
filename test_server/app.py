from flask import Flask, request, jsonify
from ecdsa import VerifyingKey, SECP256k1, util
import hashlib

app = Flask(__name__)

def recover_public_key(signature, message_hash):
    public_key_point = util.sigdecode_string(signature, SECP256k1.order)
    public_key = VerifyingKey.from_public_point(public_key_point, curve=SECP256k1)
    return public_key

def sha256_hash(message):
    sha256 = hashlib.sha256()
    sha256.update(message.encode('utf-8'))
    hashed_message = sha256.digest()
    return hashed_message

@app.route('/verify_signature', methods=['POST'])
def verify_signature():
    try:
        message = request.form['message']
        signature_string = request.form['signature']

        # Convert the signature string back to components
        r_str, s_str = signature_string.split(":")
        r, s = int(r_str), int(s_str)

        # Recover the public key from the signature
        public_key = recover_public_key(util.sigencode_string((r, s), SECP256k1.order), sha256_hash(message))

        # Verify the recovered public key against the original message and signature
        if public_key.verify(util.sigencode_string((r, s), SECP256k1.order), sha256_hash(message)):
            return jsonify({"result": "Signature verification successful"}), 200
        else:
            return jsonify({"result": "Signature verification failed"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
