from server.utils.send_http_request import send_http_request
import json


def balance(address):

    wallets = send_http_request("GET", address, "balance", {})["wallets"]
    print(json.dumps(wallets, indent=4))

    # for wallet in wallets:
    #     print(wallet)
    # # for key, value in balance.items():
    # #     print(key, value)
