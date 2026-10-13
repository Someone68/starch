import keyring as kr
from nacl.public import PrivateKey

SERVICE_NAME = "starch"


def get_token(ip: str, username: str) -> str | None:
    return kr.get_password(SERVICE_NAME, ip + "|" + username + "|token")


def get_private_key(ip: str, username: str) -> str | None:
    return kr.get_password(SERVICE_NAME, ip + "|" + username + "|private_key")


def set_token(ip: str, username: str, password: str) -> None:
    kr.set_password(SERVICE_NAME, ip + "|" + username, password)


def set_private_key(ip: str, username: str, private_key: PrivateKey) -> None:
    kr.set_password(
        SERVICE_NAME, ip + "|" + username + "|private_key", str(private_key)
    )


def del_token(ip: str, username: str) -> None:
    kr.delete_password(SERVICE_NAME, ip + "|" + username + "|token")


def del_private_key(ip: str, username: str) -> None:
    kr.delete_password(SERVICE_NAME, ip + "|" + username + "|private_key")
