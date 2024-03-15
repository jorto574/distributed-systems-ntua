from Crypto.PublicKey import RSA
from hashlib import sha256


def generate_key_pairs():
    keyPair = RSA.generate(bits=2048)
    public_key = [hex(keyPair.n), hex(keyPair.e)]
    private_key = [hex(keyPair.n), hex(keyPair.d)]
    return public_key, private_key


def sign_message(message, private_key):
    message_hash = int.from_bytes(
        sha256(message.encode("utf-8")).digest(), byteorder="big"
    )
    signature = pow(message_hash, int(private_key[1], 16), int(private_key[0], 16))
    return hex(signature)


def verify_signature(signature, public_key, message):
    hash = int.from_bytes(sha256(message.encode("utf-8")).digest(), byteorder="big")
    hash_from_signature = pow(
        int(signature, 16), int(public_key[1], 16), int(public_key[0], 16)
    )
    return hash == hash_from_signature


if __name__ == "__main__":
    public_key, private_key = generate_key_pairs()
    message = "Hello World!!!"
    signature = sign_message(message, private_key)

    print("private key: " + str(private_key))
    print("public key:  " + str(public_key))
    print("signature: " + str(signature))
    print("verify signature: " + str(verify_signature(signature, public_key, message)))
