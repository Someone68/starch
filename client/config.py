from dataclasses import asdict, dataclass, field
from json import JSONDecodeError
from pathlib import Path

import json5
from platformdirs import PlatformDirs

dirs = PlatformDirs("starch", "starch")
CONFIG_PATH = Path(dirs.user_config_path) / "config.jsonc"


@dataclass
class Account:
    username: str | None = None


@dataclass
class Config:
    active_server: str | None = None
    servers: dict[str, Account] = field(default_factory=dict)

    @property
    def account(self) -> Account | None:
        if self.active_server is None:
            return None
        return self.servers.setdefault(self.active_server, Account())

    def add_server(self, ip: str) -> None:
        self.servers.setdefault(ip, Account())
        self.active_server = ip

    @classmethod
    def load(cls) -> "Config":
        try:
            raw = json5.loads(CONFIG_PATH.read_text())
            return cls(
                active_server=raw.get("active_server"),
                servers={
                    url: Account(**acc) for url, acc in raw.get("servers", {}).items()
                },
            )
        except (FileNotFoundError, JSONDecodeError, TypeError, AttributeError):
            return cls()

    def save(self) -> None:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json5.dumps(asdict(self), indent=2))
