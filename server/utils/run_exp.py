from utils.send_http_request import send_http_request
import re
import time

def run_exp_backend(node_id, node_address, bootstrap_addr, node_num):
    start_time = time.time()

    with open(f"../input_{node_num}/trans{node_id}.txt", 'r') as file:
        for line in file:
            match = re.match(r'id(\d+)\s(.+)', line)
            if match:
                recipient_id = match.group(1)
                message_body = match.group(2).strip()

                payload = {
                    "type": "message",
                    "body": message_body,
                    "recipient_id": int(recipient_id)
                }

                # TODO : may a thread is needed here
                response = send_http_request("POST", node_address, "send_transaction", payload)
    
    end_time = time.time()
    time_taken = end_time - start_time

    payload = {
        "time": time_taken,
        "node_id": node_id
    }

    send_http_request("POST", bootstrap_addr, "endExp", payload)
