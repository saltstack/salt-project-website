"""
Shared helpers for blog-post tooling (scripts/validate-tags.py,
scripts/new-blog-post.py) — approved tag taxonomy, release-track lookup,
and the release-log (scripts/release-log.toml).
"""

import os
import tomllib

SCRIPTS_DIR = os.path.dirname(__file__)
TAGS_FILE = os.path.join(SCRIPTS_DIR, "tags.toml")
RELEASES_FILE = os.path.join(SCRIPTS_DIR, "releases.toml")
RELEASE_LOG_FILE = os.path.join(SCRIPTS_DIR, "release-log.toml")
HUGO_CONFIG_FILE = os.path.join(SCRIPTS_DIR, "..", "hugo.toml")


def load_approved_tags() -> set[str]:
    with open(TAGS_FILE, "rb") as f:
        data = tomllib.load(f)
    return set(data["approved_tags"])


def load_releases() -> dict[str, str]:
    with open(RELEASES_FILE, "rb") as f:
        data = tomllib.load(f)
    return dict(data["releases"])


def load_release_log() -> list[dict]:
    if not os.path.exists(RELEASE_LOG_FILE):
        return []
    with open(RELEASE_LOG_FILE, "rb") as f:
        data = tomllib.load(f)
    return data.get("releases", [])


def append_release_log(entries: list[dict]) -> None:
    with open(RELEASE_LOG_FILE, "a", encoding="utf-8") as f:
        for entry in entries:
            f.write("[[releases]]\n")
            f.write(f'version = "{entry["version"]}"\n')
            f.write(f'url = "{entry["url"]}"\n')
            f.write(f'date = "{entry["date"]}"\n\n')


def load_base_url() -> str:
    with open(HUGO_CONFIG_FILE, "rb") as f:
        data = tomllib.load(f)
    return data["baseURL"].rstrip("/")
