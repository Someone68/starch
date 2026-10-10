from urllib.parse import urlsplit

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
