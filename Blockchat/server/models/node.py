class Node:
    def __init__(self, id, address, public_key):
        self.id = (id,)
        self.address = address
        # self.ip_address = ip_address,
        # self.port = port,
        self.public_key = public_key
