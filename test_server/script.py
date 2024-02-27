from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey

privateKey = PrivateKey()
publicKey = privateKey.publicKey()

message = "My test message"

# Generate Signature
signature = Ecdsa.sign(message, privateKey)
print(signature)

# To verify if the signature is valid
print(Ecdsa.verify(message, signature, publicKey))