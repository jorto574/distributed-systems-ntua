from models.block import Block
from models.transaction import Transaction
from hashlib import sha256


class Blockchain:
    def __init__(self, block_list: list[Block], capacity):
        self.block_list = block_list
        self.transaction_inbox = {}
        self.capacity = capacity

    def add_block(self, block):
        self.block_list.append(block)

    def add_block():
        pass

    # this method gets called after the current block is validated
    def update_inbox():
        pass

    def get_blocks(self):
        return self.block_list

    def to_dict(self):
        return {"blocks": [block.to_dict() for block in self.block_list]}

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

    def create_block_hash(self):
        transactions_string = ""
        transaction_inbox_list = list(self.transaction_inbox.values())
        for transaction in transaction_inbox_list:
            transaction_string += transaction.create_transaction_string()
        block_string = (
            str(self.index)
            + str(self.timestamp)
            + str(transactions_string)
            + str(self.validator)
        )

        sha256_hash_object = sha256()
        sha256_hash_object.update(block_string.encode("utf-8"))
        block_string_hashed = sha256_hash_object.hexdigest()

        return block_string_hashed
