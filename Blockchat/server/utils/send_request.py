import requests


def send_request(method, address, endpoint, payload=None):
    try:
        url = f"http://{address}/{endpoint}"
        if method == "GET":
            response = requests.get(url, params=payload)
        elif method == "POST":
            response = requests.post(url, json=payload)
        elif method == "PUT":
            response = requests.put(url, json=payload)
        elif method == "DELETE":
            response = requests.delete(url)

        if response.status_code == 200:
            try:
                return response.json()  # Attempt to parse JSON response
            except ValueError:
                return response.text  # Return response text if JSON parsing fails
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return None
