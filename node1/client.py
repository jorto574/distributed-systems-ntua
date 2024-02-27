import argparse
from transaction import Transaction

def send_transaction(recipient_address, message):
    sender_address = "sender_public_key"
    receiver_address = recipient_address
    type_of_transaction = "coins"
    amount = 10.0
    signature = "abc123"

    new_transaction = Transaction(sender_address, receiver_address, type_of_transaction, amount, message, signature)
    print(f'Sending transaction to {recipient_address}: {message}')

def stake_amount(amount):
    # Implement your logic for staking a certain amount
    print(f'Staking {amount} coins')

def view():
    # Implement your logic for viewing blockchain information
    print('Viewing blockchain information')

def show_help():
    # Implement your logic to display help information
    print('Usage:')
    print('  t <recipient_address> <message>   Send a transaction')
    print('  stake <amount>                   Stake a certain amount')
    print('  view                             View blockchain information')
    print('  help                             Display this help message')

def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Blockchain CLI')
    parser.add_argument('command', choices=['t', 'stake', 'view', 'help'], help='Command to execute')

    # Define arguments specific to each command
    parser.add_argument('--recipient_address', type=str, help='Recipient address (for "t" command)')
    parser.add_argument('--message', type=str, help='Message to send (for "t" command)')
    parser.add_argument('--amount', type=float, help='Amount to stake (for "stake" command)')

    args = parser.parse_args()
    return args

def main():
    args = parse_command_line_arguments()

    if args.command == 't':
        send_transaction(args.recipient_address, args.message)
    elif args.command == 'stake':
        stake_amount(args.amount)
    elif args.command == 'view':
        view()
    elif args.command == 'help':
        show_help()

if __name__ == "__main__":
    main()
