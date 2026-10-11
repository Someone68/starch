from dataclasses import asdict, dataclass
from pathlib import Path

import json5
from platformdirs import PlatformDirs

dirs = PlatformDirs("starch", "starch")
CONFIG_PATH = Path(dirs.user_config_path) / "config.jsonc"


@dataclass
class Config:
    server_ip: str | None = None

    @classmethod
    def load(cls) -> "Config":
        try:
            return cls(**json5.loads(CONFIG_PATH.read_text()))
        except FileNotFoundError:
            return cls()

    def save(self) -> None:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json5.dumps(asdict(self), indent=2))
