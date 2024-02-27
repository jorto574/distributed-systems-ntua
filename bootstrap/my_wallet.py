from crypto import generate_key_pairs, sign_message, verify_signature
from transaction import Transaction

class MyWallet:
    def __init__(self, amount):
        self.public_key, self.private_key = generate_key_pairs()
        self.amount = amount

    def get_amount(self):
        return self.amount
    
    def set_amount(self, amount):
        self.amount = amount

    def get_public_key(self):
        return self.public_key
    
    def create_transaction(self, sender_address, receiver_address, type_of_transaction, amount, message):
        new_transaction = Transaction(sender_address, receiver_address, type_of_transaction, amount, message, None)

        def sign_transaction(transaction):
            message_to_sign = transaction.create_transaction_string()
            signature = sign_message(message_to_sign, self.private_key)
            return signature
        
        signature = sign_transaction(self, new_transaction)
        signed_transaction = Transaction(sender_address, receiver_address, type_of_transaction, amount, message, signature)
        return signed_transaction

    # TODO validation includes checking if amount of sender is enough
    def validate_transaction(transaction):
        def verify_transaction_signature():
            
            return verify_signature(transaction.get_signature, transaction.get_sender_address(), transaction.create_transaction_string())
        
        return verify_transaction_signature()
        
my_wallet = MyWallet(0)