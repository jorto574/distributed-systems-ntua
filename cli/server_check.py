import requests


def server_check(address):

    def request(address):
        url = f"http://{address}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True, response.text
            else:
                return False, f"Server returned status code: {response.status_code}"
        except requests.ConnectionError:
            return False, "Failed to connect to the server"
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    is_up, message = request(address)
    if is_up:
        print(message + "\n")
        return is_up
    else:
        print("Server is down:", message)
        return is_up
