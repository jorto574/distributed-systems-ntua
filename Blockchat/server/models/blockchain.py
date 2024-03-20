from models.block import Block
from models.transaction import Transaction


class Blockchain:
    def __init__(self, block_list: list[Block], capacity):
        self.block_list = block_list
        self.transaction_inbox = {}
        self.blockchain_transactions = {}
        self.capacity = capacity

    def add_block(self, block):
        self.block_list.append(block)

    # this method gets called after the current block is validated
    def update_inbox():
        pass

    def get_blocks(self):
        return self.block_list

    def to_dict(self):
        return {
            "blocks": [block.to_dict() for block in self.block_list],
            "transactions": [
                transaction.to_dict() for transaction in self.transaction_inbox.values()
            ],
        }

    @classmethod
    def from_dict(cls, blockchain_dict, capacity):
        block_list = [
            Block.from_dict(block_dict) for block_dict in blockchain_dict["blocks"]
        ]
        return cls(block_list, capacity)

    def validate_chain(self):
        pass

    def view(self):
        pass
