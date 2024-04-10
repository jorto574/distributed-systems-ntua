import cmd2
from dotenv import load_dotenv
import os
import sys
import argparse

from cli.stake import stake
from cli.utils import show_help, print_logo
from cli.send_coins import send_coins
from cli.send_message import send_message
from cli.view import view
from cli.server_check import server_check
from cli.view import view
from cli.balance import balance
from cli.conversations import conversations
from cli.start_exp import start_exp

# parser = argparse.ArgumentParser(description='')
# parser.add_argument('id', type=int, help='Node id')
# args = parser.parse_args()

# load_dotenv(f"{os.path.dirname(os.path.abspath(__file__))}/config/config{args.id}.env")

# url = os.environ.get("URL")
# port = os.environ.get("PORT")
# address = url + ":" + port


class BlockchatCLI(cmd2.Cmd):
    def __init__(self, node_id):
        load_dotenv(f"{os.path.dirname(os.path.abspath(__file__))}/config/config{node_id}.env")
        url = os.environ.get("URL")
        port = os.environ.get("PORT")
        self.address = url + ":" + port
        super().__init__()
        print_logo()
        if not server_check(self.address):
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
            send_coins(self.address, recipient_id, amount)
        except:
            print("Usage:")
            print("  t <recipient_id> <amount>       Send coins")

    def do_m(self, arg):
        """Send a message"""
        try:
            args = arg.split()
            recipient_id = args[0]
            message = " ".join(args[1:])
            send_message(self.address, recipient_id, message)
        except:
            print("Usage:")
            print("  m <recipient_id> <message>       Send a message")

    def do_stake(self, arg):
        """Stake a certain amount"""
        try:
            args = arg.split()
            amount = args[0]
            stake(self.address, amount)
        except:
            print("Usage:")
            print("  Stake <amount>       Stake a certain amount")

    def do_view(self, arg):
        """View command"""
        view(self.address)

    def do_balance(self, args):
        balance(self.address)

    def do_chat(self, args):
        conversations(self.address)

    def do_start_exp(self,args):
        start_exp(self.address)
    

if __name__ == "__main__":
    node_id = sys.argv[1]
    cli = BlockchatCLI(node_id)
    cli.cmdloop()
