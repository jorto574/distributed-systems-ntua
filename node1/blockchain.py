class Blockchain:
    def __init__(self, block_list):
        self.block_list = block_list

    def add_block(self, block):
        self.block_list.append(block)

    def validate_chain(self):
        pass

    def view(self):
        pass
