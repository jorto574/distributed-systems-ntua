from ecdsa import SigningKey, SECP256k1
import hashlib

def generate_private_key():
    private_key = SigningKey.generate(curve=SECP256k1)
    return private_key

def generate_public_key(private_key):
    public_key = private_key.get_verifying_key()
    return public_key

def sign_message(message, private_key):
    message_hash = hashlib.sha256(message).digest()
    signature = private_key.sign(message_hash)
    return signature

def verify_signature(signature, public_key, message):
    try:
        return public_key.verify(signature, message)
    except:
        return False

if __name__ == "__main__":
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    message = "Hello World!!!"
    signature = sign_message(message, private_key)
    print(public_key)

    print("private key: " + str(private_key.to_string().hex()))
    print("public key: " + str(public_key.to_string("compressed").hex()))
    print("signature:" + str(signature.hex()))
    print("verify signature: "+ str(verify_signature(signature, public_key, message)))