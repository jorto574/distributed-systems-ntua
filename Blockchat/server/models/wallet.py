class Wallet:
    def __init__(self, node_id, address, public_key, amount):
        self.node_id = node_id
        self.address = address
        self.public_key = public_key
        self.amount = amount

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "public_key": self.public_key,
            "amount": self.amount,
            "address": self.address
        }

    def get_amount(self):
        return self.amount
    
    def set_amount(self, amount):
        self.amount = amount

    def get_public_key(self):
        return self.public_key

    def sign_transaction(self, transaction):
        pass
