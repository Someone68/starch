from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, cast
from urllib.parse import urlsplit

if TYPE_CHECKING:
    from main import Starch

from textual.screen import Screen

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


def normalize_url(raw: str) -> str:
    url = raw.strip()
    if "://" not in url:
        host = urlsplit(f"//{url}").hostname or ""
        scheme = "http" if host in LOCAL_HOSTS else "https"
        url = f"{scheme}://{url}"

    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError(f"Invalid server URL: {raw!r}")
    return url.rstrip("/")


class StarchScreen(Screen):
    @property
    def main(self) -> "Starch":
        return cast("Starch", self.app)


@dataclass
class AuthResult:
    step: Literal["signin", "register"]
    status: int
    server: str
    username: str
    token: str | None = None


AUTH_ERRORS = {
    ("signin", 401): "Incorrect username or password.",
    ("register", 409): "Username has already been taken.",
    ("register", 422): "Username or password is invalid.",
}
