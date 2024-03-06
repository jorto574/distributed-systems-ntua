from models.block import Block
from models.transaction import Transaction


class Blockchain:
    def __init__(self, block_list: list[Block]):
        self.block_list = block_list

    def add_block(self, block):
        self.block_list.append(block)

    def get_blocks(self):
        return self.block_list

    def to_dict(self):
        return {"blocks": [block.to_dict() for block in self.block_list]}

    def add_transaction(self, transaction: Transaction):
        last_block = self.block_list[-1]
        # TODO: check if last block is full. if true create a new block.
        last_block.add_transaction(transaction)

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
