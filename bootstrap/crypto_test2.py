from Crypto.PublicKey import RSA

keyPair = RSA.generate(bits=1024)
print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")

pk = hex(keyPair.n)
print("here", int(pk, 16))

print(f"Public key:  (n={(keyPair.n)}, e={(keyPair.e)})")
print(f"Private key: (n={(keyPair.n)}, d={(keyPair.d)})")

# RSA sign the message
msg = b'A message for signing'
from hashlib import sha512
hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
signature = pow(hash, keyPair.d, keyPair.n)
print("Signature:", (signature))