"""Paths of the repository and the local configuration (local.toml, not committed).

local.toml names where the data is on this machine; the template is local.example.toml. Paths in it are
relative to the repository root. Nothing in it is ever written into a catalogue entry, run record or -meta
file (kg-commons 0018: no local paths in what is published).
"""

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog"
DECISIONS = ROOT / "docs" / "decisions"
GENERATORS = ROOT / "generators"
LOCAL = ROOT / "local.toml"


class ConfigError(Exception):
    pass


class Config:
    def __init__(self, data, source):
        self.data = data
        self.source = source   # the file read, or None

    def path(self, key):
        """A configured directory as an absolute path, or None if it is not configured."""
        value = self.data.get(key)
        return (ROOT / value).resolve() if isinstance(value, str) else None

    def paths(self, key):
        value = self.data.get(key, [])
        return [(ROOT / v).resolve() for v in value] if isinstance(value, list) else []

    def require(self, key):
        """A configured directory; raises ConfigError with a hint if it is missing."""
        p = self.path(key)
        if p is None:
            where = self.source.name if self.source else "local.toml (copy local.example.toml)"
            raise ConfigError(f"'{key}' is not configured in {where}")
        return p

    @property
    def store(self):
        return self.path("store")

    def store_of(self, slug, required=True):
        """The store a dataset's versions are in: the internal store for an internal dataset (catalogue field
        `internal`, decision 0023), else the store. required: raise ConfigError if it is not configured."""
        if not hasattr(self, "_internal"):
            from . import catalog
            self._internal = {s for s, e in catalog.Catalog().entries.items() if e.internal}
        key = "internal_store" if slug in self._internal else "store"
        return self.require(key) if required else self.path(key)

    @property
    def build(self):
        return self.path("build")


def load(path=LOCAL):
    if not path.exists():
        return Config({}, None)
    try:
        return Config(tomllib.loads(path.read_text(encoding="utf-8")), path)
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"{path.name}: {e}") from None
