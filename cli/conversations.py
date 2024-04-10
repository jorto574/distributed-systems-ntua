from server.utils.send_http_request import send_http_request
import json


def conversations(address):

    conversations = send_http_request("GET", address, "conversations", {})[
        "conversations"
    ]
    print(json.dumps(conversations, indent=4))
