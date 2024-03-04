import cmd2
from dotenv import load_dotenv
import os 
import sys

from cli.stake import stake
from cli.utils import show_help, print_logo
from cli.send_transaction import send_transaction
from cli.view import view
from cli.server_check import server_check

load_dotenv("config.env")

BASE_URL = os.environ.get("BASE_URL")
PORT = os.environ.get("PORT")
NODE_ID = os.environ.get("NODE_ID")

class BlockchatCLI(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        print_logo()
        if not server_check(BASE_URL,PORT):
            sys.exit()
        show_help()

    def help(self):
        """Usage info"""
        show_help()

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
