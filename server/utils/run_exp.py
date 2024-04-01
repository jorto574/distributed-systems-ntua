from utils.send_http_request import send_http_request
import re
import time

def run_exp(node_id, node_address, bootstrap_addr):
    start_time = time.time()

    with open(f"trans{node_id}.txt", 'r') as file:
        for line in file:
            match = re.match(r'id(\d+)\s(.+)', line)
            if match:
                recipient_id = 'id' + match.group(1)
                message_body = match.group(2).strip()

                # Prepare payload
                payload = {
                    "type": "message",
                    "body": message_body,
                    "recipient_id": recipient_id
                }

                # TODO : may a thread is needed here
                response = send_http_request("GET", node_address, "send_transaction", payload)
    
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken for the : {time_taken} seconds")

    payload = {
        "time": time_taken,
        "node_id": node_id
    }

    send_http_request("POST", bootstrap_addr, "endExp", payload)
