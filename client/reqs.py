import base64

import requests
from nacl.public import PrivateKey


def signin(url, username, password) -> tuple[int, str | None]:
    url = f"{url}/login"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    return (
        (response.status_code, response.json()["token"])
        if response.status_code == 200
        else (response.status_code, None)
    )


def register(url, username, password) -> tuple[int, PrivateKey | None]:
    private_key = PrivateKey.generate()
    public_b64 = base64.b64encode(bytes(private_key.public_key)).decode()
    url = f"{url}/register"
    data = {"username": username, "password": password, "public_key": public_b64}
    response = requests.post(url, json=data, timeout=10)
    return (
        (response.status_code, private_key)
        if response.status_code == 201
        else (response.status_code, None)
    )
