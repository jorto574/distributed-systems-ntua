from server.utils.send_http_request import send_http_request
import json


def balance(address):

    wallets = send_http_request("GET", address, "balance", {})["wallets"]

    for wallet in wallets:
        wallet["public_key"][0] = (
            wallet["public_key"][0][:10] + "..." + wallet["public_key"][0][-10:]
        )

    print(json.dumps(wallets, indent=4))

    # for wallet in wallets:
    #     print(wallet)
    # # for key, value in balance.items():
    # #     print(key, value)
