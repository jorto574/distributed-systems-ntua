import os
from flask import Flask
from dotenv import load_dotenv
import argparse

from utils.init_utils import init_bootstrap, init_node

from internal.home import home_bp
from internal.show_state import state_bp
from internal.send_transaction import send_transaction_bp

# from internal.stake import stake_bp
from internal.view import view_bp
from internal.balance import balance_bp
from internal.conversations import conversations_bp
from internal.exp_signal import exp_signal_bp

from external.talk_to_bootstrap import talk_to_bootstrap_bp
from external.receive_init_from_bootstrap import receive_init_from_bootstap_bp
from external.validate_transaction import validate_transaction_bp
from external.validate_block import validate_block_bp
from external.run_exp import run_exp_bp
from external.end_exp import end_exp_bp

app = Flask(__name__)

parser = argparse.ArgumentParser(description='')
parser.add_argument('id', type=int, help='Node id')
args = parser.parse_args()

previous_directory_full_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
load_dotenv(f"{previous_directory_full_path}/config{args.id}.env")

URL = os.environ.get("URL")
PORT = os.environ.get("PORT")
CAPACITY = os.environ.get("CAPACITY")
app.config["capacity"] = CAPACITY
app.config["bootstrap_addr"] = os.environ.get("BOOTSTRAP_ADDR")
app.config["node_num"] = int(os.environ.get("NODE_NUM"))
app.config["is_bootstrap"] = os.environ.get("IS_BOOTSTRAP")
app.config["node_count"] = 0
app.config["start_time"] = None
app.config["times"] = {}

# Internal Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(state_bp)
app.register_blueprint(send_transaction_bp)
app.register_blueprint(exp_signal_bp)

# app.register_blueprint(stake_bp)
app.register_blueprint(view_bp)
app.register_blueprint(balance_bp)
app.register_blueprint(conversations_bp)

# External Blueprints
if app.config["is_bootstrap"] == "1":
    app.register_blueprint(talk_to_bootstrap_bp)
else:
    app.register_blueprint(receive_init_from_bootstap_bp)
app.register_blueprint(validate_transaction_bp)
app.register_blueprint(validate_block_bp)
app.register_blueprint(run_exp_bp)
app.register_blueprint(end_exp_bp)


if __name__ == "__main__":

    if app.config["is_bootstrap"] == "1":
        my_state = init_bootstrap(URL, PORT, app.config["node_num"], CAPACITY)
        app.config["my_state"] = my_state
    else:
        app.config["my_state"] = None
        my_wallet = init_node(URL, PORT, app.config["bootstrap_addr"])
        app.config["my_wallet"] = my_wallet

    app.run(debug=False, host=URL, port=PORT)
