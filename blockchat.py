import cmd2
from dotenv import load_dotenv
import os
import sys

from cli.stake import stake
from cli.utils import show_help, print_logo
from cli.send_coins import send_coins
from cli.send_message import send_message
from cli.view import view
from cli.server_check import server_check
from cli.view import view
from cli.balance import balance

load_dotenv(f"{os.path.dirname(os.path.abspath(__file__))}/config.env")

url = os.environ.get("URL")
port = os.environ.get("PORT")
address = url + ":" + port


class BlockchatCLI(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        print_logo()
        if not server_check(address):
            sys.exit()
        show_help()

    def help(self):
        """Usage info"""
        show_help()

    def do_t(self, arg):
        """Send a transaction"""
        try:
            args = arg.split()
            recipient_id = args[0]
            amount = " ".join(args[1:])
            send_coins(address, recipient_id, amount)
        except:
            print("Usage:")
            print("  t <recipient_id> <amount>       Send coins")

    def do_m(self, arg):
        """Send a message"""
        try:
            args = arg.split()
            recipient_id = args[0]
            message = " ".join(args[1:])
            send_message(address, recipient_id, message)
        except:
            print("Usage:")
            print("  m <recipient_id> <message>       Send a message")

    def do_stake(self, arg):
        """Stake a certain amount"""
        stake(arg)

    def do_view(self, arg):
        """View command"""
        view(address)

    def do_balance(self, args):
        balance(address)


if __name__ == "__main__":
    cli = BlockchatCLI()
    cli.cmdloop()
