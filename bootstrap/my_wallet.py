class MyWallet:
    def __init__(self, public_key, private_key, amount):
        self.public_key = public_key
        self.private_key = private_key
        self.amount = amount

    def get_amount(self):
        return self.amount
    
    def set_amount(self, amount):
        self.amount = amount

    def get_public_key(self):
        return self.public_key

    def sign_transaction(self, transaction):
        pass
