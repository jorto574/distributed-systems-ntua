def show_help():
    # Implement your logic to display help information
    print("Usage:")
    print("  t <recipient_id> <amount>        Send 'coins' transaction")
    print("  m <recipient_id> <message>       Send 'message' transaction")
    print("  stake <amount>                   Stake a certain amount")
    print("  view                             View last block")
    print("  balance                          View wallets info")
    print("  quit                             Exit app")
    print("  help                             Usage info")
    print("")

def print_logo():
    print(
        """
╔╗ ┬  ┌─┐┌─┐┬┌─  ╔═╗┬ ┬┌─┐┌┬┐
╠╩╗│  │ ││  ├┴┐  ║  ├─┤├─┤ │ 
╚═╝┴─┘└─┘└─┘┴ ┴  ╚═╝┴ ┴┴ ┴ ┴ 
"""
    )
