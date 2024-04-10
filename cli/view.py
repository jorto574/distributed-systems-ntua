from server.utils.send_http_request import send_http_request
import json


def view(address):

    block = send_http_request("GET", address, "view", {})["last_block"]

    for transaction in block["transactions"]:

        if transaction["receiver_public_key"] != 0:
            transaction["receiver_public_key"][0] = (
                transaction["receiver_public_key"][0][:10]
                + "..."
                + transaction["receiver_public_key"][0][-10:]
            )

        transaction["sender_public_key"][0] = (
            transaction["sender_public_key"][0][:10]
            + "..."
            + transaction["sender_public_key"][0][-10:]
        )

        transaction["signature"] = (
            transaction["signature"][:10] + "..." + transaction["signature"][-10:]
        )

    block["validator"][0] = (
        block["validator"][0][:10] + "..." + block["validator"][0][-10:]
    )
    print(json.dumps(block, indent=4))
    # for key, value in block.items():
    #     print(key, value)
