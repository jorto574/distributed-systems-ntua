from ecdsa import SigningKey, SECP256k1, VerifyingKey, util
import hashlib

def generate_private_key():
    private_key = SigningKey.generate(curve=SECP256k1)
    return private_key

def generate_public_key(private_key):
    public_key = private_key.get_verifying_key()
    return public_key

def sign_message(message, private_key):
    hashed_message = sha256_hash(message)
    signature = private_key.sign(hashed_message, hashfunc=hashlib.sha256)
    return signature

def recover_public_key(signature, message):
    # The 'util.sigdecode_string' method will recover the public key from the signature and message hash
    public_key = VerifyingKey.from_public_point(util.sigdecode_string(signature, SECP256k1.order, hashed_message=sha256_hash(message)), curve=SECP256k1)
    return public_key

def sha256_hash(message):
    sha256 = hashlib.sha256()
    sha256.update(message.encode('utf-8'))
    hashed_message = sha256.digest()
    return hashed_message

def verify_signature_with_recovery(signature, message):
    try:
        # Recover the public key from the signature and message
        public_key = recover_public_key(signature, message)

        # Verify the recovered public key against the original message and signature
        return public_key.verify(signature, sha256_hash(message).encode())
    except:
        return False

if __name__ == "__main__":
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    message = "Hello World!!!"
    signature = sign_message(message, private_key)
    print("public key: " + str(public_key.to_string("compressed").hex()))
    print("signature:" + str(signature.hex()))
    print("verify signature with recovery: " + str(verify_signature_with_recovery(signature, message)))
