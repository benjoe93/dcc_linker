import json

import requests

from .constants import HostApps


class Client:
    def __init__(self, origin: str = HostApps.undefined) -> None:
        self.origin: str = origin

    def send_command(self, target: int, func_name: str, parameters: dict = {}) -> bool:

        url: str = f"http://localhost:{target}"
        payload = {
            "func": func_name,
            "params": parameters,
            "origin": self.origin,
        }

        response: requests.Response = requests.request("POST", url, data=json.dumps(payload))

        if response.status_code >= 200 and response.status_code < 300:
            print(f"{response.status_code}: {response.text}")
            return True
        else:
            print(f"{response.status_code}: {response.json}")
            return False
