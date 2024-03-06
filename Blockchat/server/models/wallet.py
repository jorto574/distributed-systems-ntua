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
            "address": self.address,
        }

    @classmethod
    def from_dict(cls, wallet_dict):
        return cls(
            wallet_dict["node_id"],
            wallet_dict["address"],
            wallet_dict["public_key"],
            wallet_dict["amount"],
        )
