import keyring as kr

SERVICE_NAME = "starch"


def get_token(ip: str) -> str | None:
    return kr.get_password(SERVICE_NAME, ip)


def set_token(ip: str, password: str) -> None:
    kr.set_password(SERVICE_NAME, ip, password)


def del_token(ip: str) -> None:
    kr.delete_password(SERVICE_NAME, ip)
