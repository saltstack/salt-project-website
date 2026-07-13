#!/usr/bin/env python3
"""
Generate a new blog post file in content/blog, following the site's
standardized file naming, front matter, and body content conventions.

Post types:
  release      New Salt GA release (one or more versions).
  rc           New Salt release candidate (one version).
  security     New Salt security/CVE advisory (one or more versions).
  announcement General news/announcement post.

The release track (LTS/STS/RC) for each Salt major version is looked up in
scripts/releases.toml — add a major version there before generating a
release, rc, or security post for it.

`release` and `security` are checked against scripts/release-log.toml (a
log of every version ever announced): a version that's already been
published is rejected, and a version must be the next expected patch
number for its major line (e.g. after 3006.27, the next 3006.x release
must be 3006.28). On success, the new version(s) are appended to the log.

Usage:
  python3 scripts/new-blog-post.py release --version 3008.2
  python3 scripts/new-blog-post.py release --version 3008.0 --version 3006.25
  python3 scripts/new-blog-post.py rc --version 3008 --rc 1
  python3 scripts/new-blog-post.py security --version 3008.2
  python3 scripts/new-blog-post.py security --version 3006.12 --version 3007.4
  python3 scripts/new-blog-post.py announcement --title "..." --summary "..." --tags community

All generated posts default to `draft: true`. Pass --publish to omit it.
"""

import argparse
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from _blog_common import (  # noqa: E402
    load_approved_tags,
    load_releases,
    load_release_log,
    append_release_log,
    load_base_url,
)

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")

TRACK_FULL_NAME = {
    "LTS": "Long-Term Support (LTS)",
    "STS": "Short-Term Support (STS)",
}

MONTH_ABBR = [
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC",
]


class BlogPostError(Exception):
    """A user-facing error — printed as `error: ...` and exits 1."""


def parse_date(value: str | None) -> date:
    if value is None:
        return date.today()
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise BlogPostError(f"invalid --date '{value}' — expected YYYY-MM-DD")


def major_of(version: str) -> str:
    return version.split(".", 1)[0]


def track_of(version: str, releases: dict[str, str]) -> str:
    major = major_of(version)
    if major not in releases:
        raise BlogPostError(
            f"major version '{major}' not found in scripts/releases.toml — "
            "add it before generating this post."
        )
    return releases[major]


def validate_new_version(version: str, log_entries: list[dict]) -> None:
    """Reject a version that's already been announced, or that isn't the
    next expected patch number for its major line (per the release log)."""
    for entry in log_entries:
        if entry["version"] == version:
            raise BlogPostError(
                f"version '{version}' has already been announced: "
                f"{entry['url']} (published {entry['date']})"
            )

    major = major_of(version)
    minor_str = version[len(major) + 1:] if "." in version else None
    try:
        minor = int(minor_str) if minor_str is not None else None
    except ValueError:
        minor = None

    existing_minors = []
    for entry in log_entries:
        if major_of(entry["version"]) != major:
            continue
        try:
            existing_minors.append(int(entry["version"][len(major) + 1:]))
        except ValueError:
            continue

    if existing_minors and minor is not None:
        expected = max(existing_minors) + 1
        if minor != expected:
            raise BlogPostError(
                f"version '{version}' is not the next expected release for "
                f"major '{major}' — last published was "
                f"'{major}.{max(existing_minors)}', expected '{major}.{expected}'."
            )


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


def dashed(version: str) -> str:
    return version.replace(".", "-")


# ---------------------------------------------------------------------------
# Front matter rendering
# ---------------------------------------------------------------------------

def build_front_matter(
    *,
    draft: bool,
    title: str,
    summary: str,
    post_date: date,
    author: str | None = None,
    url: str | None = None,
    image: str | None = None,
    tags: list[str],
) -> str:
    fields: list[tuple[str, object]] = []
    if draft:
        fields.append(("draft", True))
    fields.append(("title", title))
    fields.append(("summary", summary))
    fields.append(("date", post_date.isoformat()))
    if author is not None:
        fields.append(("author", author))
    if url is not None:
        fields.append(("url", url))

    lines = ["---"]
    for key, value in fields:
        if isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        else:
            lines.append(f'{key}: "{value}"')
    if image is not None:
        lines.append(f"image: {image}")
        lines.append("image_alt:")
    lines.append("tags:")
    for tag in tags:
        lines.append(f"    - {tag}")
    lines.append("---\n")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# release
# ---------------------------------------------------------------------------

INSTALL_UPGRADE_NOTES = """\
## Installation & Upgrade Notes

Users can install Salt {version} via PyPI or through our official package repositories.

* **Package Repo:** Packages are available here:
  * [deb](https://packages.broadcom.com/artifactory/saltproject-deb/)
  * [rpm](https://packages.broadcom.com/artifactory/saltproject-rpm/)
  * [mac](https://packages.broadcom.com/artifactory/saltproject-generic/macos/{version}/)
  * [win](https://packages.broadcom.com/artifactory/saltproject-generic/windows/{version}/)
  * [onedir](https://packages.broadcom.com/artifactory/saltproject-generic/onedir/{version}/)
* **Install Guide:** Refer to our official instructions for [Installing Salt](https://docs.saltproject.io/salt/install-guide/en/latest/index.html).
* **PyPI Source:** Download the package directly via [PyPI](https://pypi.org/project/salt/{version}/)

| IMPORTANT |
| --------- |
| While Salt supports differing versions between the Master and Minions during transitional periods, it is **highly recommended to upgrade your Salt Master first** to prevent compatibility issues. |

## Reporting Issues & Feedback

A massive thank you to everyone in the community who tested the Release Candidates and helped us cross the finish line!

If you encounter any unexpected behavior, bugs, or packaging issues with this GA release, please let us know right away by opening an issue:

[**Open a GitHub Issue**](https://github.com/saltstack/salt/issues/new/choose)

Thank you for being a vital part of the Salt Project community. Happy automating!
"""


def cmd_release(args: argparse.Namespace, releases: dict[str, str]) -> str:
    versions = args.version
    tracks = [track_of(v, releases) for v in versions]
    post_date = parse_date(args.date)

    log_entries = load_release_log()
    for v in versions:
        validate_new_version(v, log_entries)

    if len(versions) == 1:
        version, track = versions[0], tracks[0]
        major = major_of(version)
        is_ga = version.split(".", 1)[1] == "0" if "." in version else False

        title = f"Salt {version} {track} Now {'Generally Available' if is_ga else 'Available'}"
        summary = f"The Salt Project has just released {version} ({track} Release)."

        if is_ga:
            full_name = TRACK_FULL_NAME.get(track, track)
            body = (
                f"The Salt Project is thrilled to announce the official general "
                f"availability (GA) release of Salt {version} {track}.\n\n"
                f"This milestone marks the culmination of extensive development, "
                f"testing, and invaluable feedback from our community throughout "
                f"the Release Candidate cycles. Salt {version} is a {full_name} "
                f"release, bringing a hardened foundation, crucial bug fixes, and "
                f"performance enhancements designed to power your infrastructure "
                f"with maximum stability.\n\n"
                f"## What's New in Salt {version}?\n\n"
                f"Whether you are prioritizing long-term enterprise stability or "
                f"eager to leverage the latest optimizations, this release is "
                f"ready for production environments.\n\n"
                f"* **The Tag:** Check out the official ``v{version}`` tag on "
                f"[GitHub](https://github.com/saltstack/salt/releases/tag/v{version})\n"
                f"* **Release Notes:** View the release notes on "
                f"[GitHub](https://github.com/saltstack/salt/blob/{major}.x/doc/topics/releases/{version}.md)\n\n"
            )
        else:
            body = (
                f"The Salt Project has just released the {version} {track} "
                f"bugfix version of Salt.\n\n"
                f"* **Release Notes:** View the release notes on "
                f"[GitHub](https://github.com/saltstack/salt/blob/{major}.x/doc/topics/releases/{version}.md)\n"
                f"* **Changelogs:** https://github.com/saltstack/salt/blob/v{version}/CHANGELOG.md\n"
                f"* **The Tag:** Check out the official ``v{version}`` tag on "
                f"[GitHub](https://github.com/saltstack/salt/releases/tag/v{version})\n\n"
            )

        body += INSTALL_UPGRADE_NOTES.format(version=version)
        slug = f"salt-{dashed(version)}-available"
    else:
        joined = " and ".join(f"{v} {t}" for v, t in zip(versions, tracks))
        title = f"Salt {joined} Now Available"
        summary = f"The Salt Project has just released {joined}."

        body = ""
        for version, track in zip(versions, tracks):
            major = major_of(version)
            body += (
                f"### Salt {version} {track}\n\n"
                f"* **Release Notes:** View the release notes on "
                f"[GitHub](https://github.com/saltstack/salt/blob/{major}.x/doc/topics/releases/{version}.md)\n"
                f"* **Changelogs:** https://github.com/saltstack/salt/blob/v{version}/CHANGELOG.md\n"
                f"* **The Tag:** Check out the official ``v{version}`` tag on "
                f"[GitHub](https://github.com/saltstack/salt/releases/tag/v{version})\n\n"
            )

        body += (
            "## Installation & Upgrade Notes\n\n"
            "Users can install Salt via PyPI or through our official package "
            "repositories.\n\n"
            "* **Install Guide:** Refer to our official instructions for "
            "[Installing Salt](https://docs.saltproject.io/salt/install-guide/en/latest/index.html).\n"
            "* **PyPI Source:** Packages are available via "
            "[PyPI](https://pypi.org/project/salt/)\n\n"
            "| IMPORTANT |\n"
            "| --------- |\n"
            "| While Salt supports differing versions between the Master and "
            "Minions during transitional periods, it is **highly recommended "
            "to upgrade your Salt Master first** to prevent compatibility "
            "issues. |\n\n"
            "## Reporting Issues & Feedback\n\n"
            "If you encounter any unexpected behavior, bugs, or packaging "
            "issues with this release, please let us know right away by "
            "opening an issue:\n\n"
            "[**Open a GitHub Issue**](https://github.com/saltstack/salt/issues/new/choose)\n\n"
            "Thank you for being a vital part of the Salt Project community. "
            "Happy automating!\n"
        )
        slug = "salt-" + "-and-".join(dashed(v) for v in versions) + "-available"

    front_matter = build_front_matter(
        draft=not args.publish,
        title=title,
        summary=summary,
        post_date=post_date,
        author="Salt Project Team",
        image="images/blog/new-release.png",
        tags=["release"],
    )
    return write_post_and_log(post_date, slug, front_matter, body, allow_suffix=False, versions=versions)


# ---------------------------------------------------------------------------
# rc
# ---------------------------------------------------------------------------

def cmd_rc(args: argparse.Namespace, releases: dict[str, str]) -> str:
    version = args.version[0]
    major = major_of(version)
    track = track_of(version, releases)
    n = args.rc
    post_date = parse_date(args.date)

    title = f"Salt {major} RC{n} is now available"
    summary = (
        f"The Salt Project has just released RC{n} (release candidate {n}) "
        f"of the Salt {major} {track}."
    )
    slug = f"salt-{major}-rc{n}-available"
    body = (
        f"The Salt Project has just released RC{n} (release candidate {n}) of the Salt {major}\n"
        f"{track}. To download and test Salt {major} RC{n}, see\n"
        f"[Install a release candidate](https://docs.saltproject.io/salt/install-guide/en/latest/topics/other-install-types/release-candidate.html)\n"
        f"in the Salt install guide.\n\n"
        f"Users can install via PyPI, packages, or use the Docker containers.\n\n"
        f"| Note  |\n"
        f"| ----- |\n"
        f"| We support differing versions between master and minions, but as "
        f"always it is recommended to upgrade your master first. |\n\n"
        f"- The tag: https://github.com/saltstack/salt/tree/v{major}.0rc{n}\n"
        f"- The PyPI Source: https://pypi.org/project/salt/{major}.0rc{n}/\n\n"
        f"If you find any issues with Salt or the packaging, open an issue here:\n"
        f"[https://github.com/saltstack/salt/issues/new/choose](https://github.com/saltstack/salt/issues/new/choose)\n"
    )

    front_matter = build_front_matter(
        draft=not args.publish,
        title=title,
        summary=summary,
        post_date=post_date,
        url=f"blog/{slug}",
        image="images/blog/new-update.png",
        tags=["release", "release-candidate"],
    )
    return write_post(post_date, slug, front_matter, body, allow_suffix=False)


# ---------------------------------------------------------------------------
# security
# ---------------------------------------------------------------------------

def cmd_security(args: argparse.Namespace, releases: dict[str, str]) -> str:
    versions = args.version
    tracks = [track_of(v, releases) for v in versions]
    post_date = parse_date(args.date)
    date_label = f"{post_date.year}-{MONTH_ABBR[post_date.month - 1]}-{post_date.day}"

    log_entries = load_release_log()
    for v in versions:
        validate_new_version(v, log_entries)

    title = f"Salt security advisory release - {date_label}"

    if len(versions) == 1:
        version, track = versions[0], tracks[0]
        summary = (
            f"The Salt Project is announcing the Salt {version} {track} CVE "
            f"release. This release addresses {{NUMBER}} CVEs, ranging from "
            f"{{LOWEST_SEVERITY}} to {{HIGHEST_SEVERITY}} in severity."
        )
        release_notes_block = _security_release_notes_block(version, track)
    else:
        joined = " and ".join(f"{v} {t}" for v, t in zip(versions, tracks))
        summary = (
            f"The Salt Project is announcing the Salt {joined} CVE releases. "
            f"This release addresses {{NUMBER}} CVEs, ranging from "
            f"{{LOWEST_SEVERITY}} to {{HIGHEST_SEVERITY}} in severity."
        )
        release_notes_block = "".join(
            _security_release_notes_block(v, t) for v, t in zip(versions, tracks)
        )

    packages_list = "\n".join(f"- {v}" for v in versions)

    body = (
        f"Salt Project Community Members!\n\n"
        f"{summary}\n\n"
        f"To download and install the latest versions of Salt, see the "
        f"[Salt install guide](https://docs.saltproject.io/salt/install-guide/en/latest/).\n\n"
        f"{release_notes_block}"
        f"Directory repository locations:\n\n"
        f"- [Salt Project Repository: Linux (RPM)](https://packages.broadcom.com/artifactory/saltproject-rpm): "
        f"Where Salt `rpm` packages are officially stored and distributed.\n"
        f"- [Salt Project Repository: Linux (DEB)](https://packages.broadcom.com/artifactory/saltproject-deb): "
        f"Where Salt `deb` packages are officially stored and distributed.\n"
        f"- [Salt Project Repository: GENERIC](https://packages.broadcom.com/artifactory/saltproject-generic): "
        f"Where Salt Windows, macOS, etc. (non-rpm, non-deb) packages are officially stored and distributed.\n"
        f"- Best-effort supported versions of Salt (non-relenv) are also available on PyPI: https://pypi.org/project/salt/\n\n"
        f"## CVE Details\n\n"
        f"### CVE-{{YYYY}}-{{NNNNN}}\n\n"
        f"- **Description:** {{Describe the vulnerability.}}\n"
        f"- **Impact:** {{Describe the impact.}}\n"
        f"- **Solution:** {{Describe the fix.}}\n"
        f"- **How to Mitigate:** Upgrade Salt to {{fixed version(s)}}\n"
        f"- **Attribution:** {{Reporter name/organization}}\n"
        f"- **Severity Rating:** {{CVSS score and vector, e.g. 7.7 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N}}\n\n"
        f"## Packages\n\n"
        f"Updated packages for the versions below can be found at "
        f"https://repo.saltproject.io for these supported versions of Salt.\n\n"
        f"{packages_list}\n\n"
        f"Thank you all for your contributions!\n\n"
        f"-- Salt Project Team\n"
    )

    front_matter = build_front_matter(
        draft=not args.publish,
        title=title,
        summary=summary,
        post_date=post_date,
        image="images/blog/new-alert.png",
        tags=["security", "release"],
    )
    return write_post_and_log(post_date, "advisory", front_matter, body, allow_suffix=True, versions=versions)


def _security_release_notes_block(version: str, track: str) -> str:
    major = major_of(version)
    return (
        f"For more details on the Salt {version} {track} release:\n"
        f"- Release notes: https://docs.saltproject.io/en/{major}/topics/releases/{version}.html\n"
        f"- Changelogs: https://github.com/saltstack/salt/blob/{major}.x/CHANGELOG.md\n\n"
    )


# ---------------------------------------------------------------------------
# announcement
# ---------------------------------------------------------------------------

def cmd_announcement(args: argparse.Namespace, approved_tags: set[str]) -> str:
    bad = [t for t in args.tags if t not in approved_tags]
    if bad:
        raise BlogPostError(
            f"unapproved tag(s): {', '.join(bad)} — see scripts/tags.toml "
            f"for the approved list."
        )

    post_date = parse_date(args.date)
    slug = slugify(args.title)

    front_matter = build_front_matter(
        draft=not args.publish,
        title=args.title,
        summary=args.summary,
        post_date=post_date,
        author=args.author,
        url=f"blog/{slug}",
        image=args.image,
        tags=args.tags,
    )
    body = "Your content goes here\n"
    return write_post(post_date, slug, front_matter, body, allow_suffix=False)


# ---------------------------------------------------------------------------
# Shared file writer
# ---------------------------------------------------------------------------

def write_post(post_date: date, slug: str, front_matter: str, body: str, *, allow_suffix: bool) -> str:
    os.makedirs(BLOG_DIR, exist_ok=True)
    base = f"{post_date.isoformat()}-{slug}"
    filename = f"{base}.md"
    path = os.path.join(BLOG_DIR, filename)

    if os.path.exists(path):
        if not allow_suffix:
            raise BlogPostError(f"{path} already exists")
        n = 1
        while True:
            filename = f"{base}-{n:02d}.md"
            path = os.path.join(BLOG_DIR, filename)
            if not os.path.exists(path):
                break
            n += 1

    with open(path, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write("\n")
        f.write(body)

    return path


def write_post_and_log(
    post_date: date, slug: str, front_matter: str, body: str, *, allow_suffix: bool,
    versions: list[str],
) -> str:
    """write_post(), then append one release-log entry per version, using the
    actual filename written (which may differ from `slug` if a same-day
    collision suffix was applied)."""
    path = write_post(post_date, slug, front_matter, body, allow_suffix=allow_suffix)
    post_slug = os.path.splitext(os.path.basename(path))[0]
    url = f"{load_base_url()}/blog/{post_slug}/"
    append_release_log([
        {"version": v, "url": url, "date": post_date.isoformat()} for v in versions
    ])
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    date_help = "Post date, YYYY-MM-DD (default: today)."
    publish_help = "Omit draft: true (default: draft)."

    p_release = subparsers.add_parser("release", help="New Salt GA release.")
    p_release.add_argument("--version", action="append", required=True, help="e.g. 3008.2 (repeatable).")
    p_release.add_argument("--date", help=date_help)
    p_release.add_argument("--publish", action="store_true", help=publish_help)

    p_rc = subparsers.add_parser("rc", help="New Salt release candidate.")
    p_rc.add_argument("--version", action="append", required=True, help="Major version, e.g. 3008.")
    p_rc.add_argument("--rc", type=int, required=True, help="RC number, e.g. 1.")
    p_rc.add_argument("--date", help=date_help)
    p_rc.add_argument("--publish", action="store_true", help=publish_help)

    p_security = subparsers.add_parser("security", help="New Salt security/CVE advisory.")
    p_security.add_argument("--version", action="append", required=True, help="e.g. 3008.2 (repeatable).")
    p_security.add_argument("--date", help=date_help)
    p_security.add_argument("--publish", action="store_true", help=publish_help)

    p_announcement = subparsers.add_parser("announcement", help="General news/announcement post.")
    p_announcement.add_argument("--title", required=True)
    p_announcement.add_argument("--summary", required=True)
    p_announcement.add_argument(
        "--tags", required=True,
        help="Comma-separated list of approved tags (see scripts/tags.toml).",
    )
    p_announcement.add_argument("--author", help="Omit for an anonymous post.")
    p_announcement.add_argument("--image", help="e.g. images/blog/new-update.png")
    p_announcement.add_argument("--date", help=date_help)
    p_announcement.add_argument("--publish", action="store_true", help=publish_help)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "rc" and len(args.version) != 1:
        parser.error("rc takes exactly one --version")

    try:
        if args.command == "announcement":
            args.tags = [t.strip() for t in args.tags.split(",") if t.strip()]
            approved_tags = load_approved_tags()
            path = cmd_announcement(args, approved_tags)
        else:
            releases = load_releases()
            if args.command == "release":
                path = cmd_release(args, releases)
            elif args.command == "rc":
                path = cmd_rc(args, releases)
            elif args.command == "security":
                path = cmd_security(args, releases)
            else:
                parser.error(f"unknown command: {args.command}")
                return 2
    except BlogPostError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"Created {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
