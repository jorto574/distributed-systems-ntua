def show_help():
    # Implement your logic to display help information
    print("Usage:")
    print("  t <recipient_id> <message>       Send a transaction")
    print("  stake <amount>                   Stake a certain amount")
    print("  view                             View blockchain information")
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
