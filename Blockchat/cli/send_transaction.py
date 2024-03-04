from server.models.transaction import Transaction

def send_transaction(recipient_address, message):
    sender_address = "sender_public_key"
    receiver_address = recipient_address
    type_of_transaction = "coins"
    amount = 10.0
    signature = "abc123"

    new_transaction = Transaction(sender_address, receiver_address, type_of_transaction, amount, message, signature)
    print(f'Sending transaction to {recipient_address}: {message}')