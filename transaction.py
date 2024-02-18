class transaction:
    def __init__(self, transaction_id, sender_address, receiver_address, type_, amount, message, nonce, signature):
        self.id = transaction_id
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.type_of_transaction = type_
        self.amount = amount
        self.message = message
        self.nonce = nonce
        self.signature = signature
