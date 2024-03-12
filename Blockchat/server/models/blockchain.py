from models.block import Block
from models.transaction import Transaction


class Blockchain:
    def __init__(self, block_list: list[Block], capacity):
        self.block_list = block_list
        self.transaction_inbox = {}
        self.capacity

    def add_block(self, block):
        self.block_list.append(block)

    def add_block():
        pass

    def update_inbox():
        pass

    def get_blocks(self):
        return self.block_list

    def to_dict(self):
        return {"blocks": [block.to_dict() for block in self.block_list]}

    def add_transaction(self, transaction: Transaction):
        sender_address = transaction.sender_address
        nonce = transaction.nonce
        key = (sender_address, nonce)
        self.transaction_inbox[key] = transaction
        if len(self.transaction_inbox) == self.capacity: 
            



    @classmethod
    def from_dict(cls, blockchain_dict):
        block_list = [
            Block.from_dict(block_dict) for block_dict in blockchain_dict["blocks"]
        ]
        return cls(block_list)

    def validate_chain(self):
        pass

    def view(self):
        pass
