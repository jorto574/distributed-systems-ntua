from server.utils.send_http_request import send_http_request
import json


def view(address):

    block = send_http_request("GET", address, "view", {})["last_block"]
    print(json.dumps(block, indent=4))
    # for key, value in block.items():
    #     print(key, value)
