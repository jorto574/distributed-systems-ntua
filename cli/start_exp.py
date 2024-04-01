from server.utils.send_http_request import send_http_request

def start_exp(address, recipient_id, amount):

    print(f" Starting app test")

    response = send_http_request("GET", address, "exp_signal", {})
    
    print(response["status"])
