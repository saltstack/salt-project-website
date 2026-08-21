"""
Shared helpers for blog-post tooling (scripts/validate-tags.py,
scripts/new-blog-post.py) — approved tag taxonomy, release-track lookup,
the release-log (scripts/release-log.toml), and body templates
(scripts/blog-templates/).
"""

import os
import string
import tomllib

SCRIPTS_DIR = os.path.dirname(__file__)
TAGS_FILE = os.path.join(SCRIPTS_DIR, "tags.toml")
RELEASES_FILE = os.path.join(SCRIPTS_DIR, "releases.toml")
RELEASE_LOG_FILE = os.path.join(SCRIPTS_DIR, "release-log.toml")
HUGO_CONFIG_FILE = os.path.join(SCRIPTS_DIR, "..", "hugo.toml")
BLOG_TEMPLATES_DIR = os.path.join(SCRIPTS_DIR, "blog-templates")


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


def render_template(name: str, /, **substitutions: str) -> str:
    """Load scripts/blog-templates/<name>.md and fill in its $placeholder
    variables. These are ordinary Markdown files -- open one directly to
    write a post by hand, with or without this tooling; `$placeholder`
    tokens (e.g. $version) are the only thing that's not literal content.

    Uses stdlib string.Template rather than str.format so a template can
    contain its own literal {curly-brace} placeholders (e.g. the CVE
    details a human fills in by hand) without colliding with substitution
    syntax.
    """
    path = os.path.join(BLOG_TEMPLATES_DIR, f"{name}.md")
    with open(path, encoding="utf-8") as f:
        template = string.Template(f.read())
    return template.substitute(**substitutions)
