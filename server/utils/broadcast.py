from flask import current_app
import requests
import time
from models.wallet import PublicWallet


def broadcast(
    endpoint: str,
    payload: dict,
    wallets: list[PublicWallet],
    my_address: str,
    verbose: bool = True,
) -> bool:
    success = True

    for wallet in wallets:
        address = wallet.node_address
        is_receiver_self = address == my_address
        if not is_receiver_self:
            node_id = wallet.node_id
            retries = 3
            delay_between_retries = 5

            while retries > 0:
                try:
                    success = True
                    response = requests.post(
                        f"http://{address}/{endpoint}", json=payload, timeout=1
                    )
                    if response.status_code == 200:
                        if verbose:
                            print(f"Broadcasted successfully to node {node_id}.")
                        break
                    else:
                        success = False
                        if verbose:
                            print(
                                f"Broadcast to node {node_id} failed with status code: {response.status_code}"
                            )

                except requests.exceptions.RequestException as e:
                    success = False
                    if verbose:
                        print(f"Error making the request: {e}")
                        print(f"Retries remaining {retries}")

                time.sleep(delay_between_retries)
                retries -= 1

                if retries == 0:
                    if verbose:
                        print(
                            f"Max retries reached. Unable to broadcast to node {node_id}."
                        )

    if success and verbose:
        print(f"Successfully broadcasted Blockchat to every node!")

    return success
