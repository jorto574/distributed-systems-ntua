import cmd2
from cli.stake import stake
from cli.utils import show_help, print_logo
from cli.send_transaction import send_transaction
from cli.view import view


class BlockchatCLI(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        print_logo()
        show_help()

    def help(self):
        """Usage info"""
        show_help()

    def do_init_node(self, arg):

        """Initialize node. If node id = 0 then the blockchain is also initialized"""
        pass  # Add functionality here

    def do_t(self, arg):
        """Send a transaction"""
        args = arg.split()
        recipient_address = args[0]
        message = ' '.join(args[1:])
        send_transaction(recipient_address, message)

    def do_stake(self, arg):
        """Stake a certain amount"""
        stake(arg)

    def do_view(self, arg):
        """View command"""
        view()


if __name__ == '__main__':
    cli = BlockchatCLI()
    cli.cmdloop()
