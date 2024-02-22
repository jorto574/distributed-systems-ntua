class Blockchain:
    def __init__(self, block_list):
        self.block_list = block_list

    def add_block(self, block):
        self.block_list.append(block)

    def get_blocks(self):
        return self.block_list

    def to_dict(self):
        return {
            "blockchain": {
                "blocks": [block.to_dict() for block in self.block_list]
            }
        }

    def validate_chain(self):
        pass

    def view(self):
        pass
