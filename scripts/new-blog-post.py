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

Post bodies are filled in from the Markdown templates in
scripts/blog-templates/ (via _blog_common.render_template) rather than
being embedded in this file. Those templates are ordinary, readable
Markdown with `$placeholder` variables (e.g. $version) -- open one
directly to see (or copy) what a generated post's body looks like, edit
one to change the wording for every future post of that type, or write a
post by hand from one without using this script at all.
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
    render_template,
)

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")

TRACK_FULL_NAME = {
    "LTS": "Long-Term Support (LTS)",
    "STS": "Short-Term Support (STS)",
}

TRACK_PLAIN_NAME = {
    "LTS": "Long-Term Support",
    "STS": "Short-Term Support",
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
            body = render_template(
                "release-ga-body", version=version, track=track, major=major, full_name=full_name,
            )
        else:
            body = render_template("release-bugfix-body", version=version, track=track, major=major)

        body += "\n" + render_template("install-upgrade-notes-versioned", version=version)
        # Every single-version release post uses this same "thanks to our
        # RC testers"/"this GA release" wording, whether it's an actual x.0
        # GA promotion or a routine bugfix patch -- confirmed against every
        # real post since this house style was adopted (3008.0/.1/.2,
        # 3006.26/.27), so this isn't a per-GA-status choice.
        body += "\n" + render_template("reporting-feedback")
        slug = f"salt-{dashed(version)}-available"
    else:
        joined = " and ".join(f"{v} {t}" for v, t in zip(versions, tracks))
        title = f"Salt {joined} Now Available"
        summary = f"The Salt Project has just released {joined}."

        body = "\n".join(
            render_template(
                "release-multi-version-block", version=v, track=t, major=major_of(v),
                full_name=TRACK_PLAIN_NAME.get(t, t),
            )
            for v, t in zip(versions, tracks)
        )
        body += "\n" + render_template("installation-notes-simple")
        body += "\n" + render_template("reporting-issues-simple")
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

    title = f"Salt {major} RC{n} Now Available"
    summary = f"The Salt Project has just released {major}.0rc{n} (Release Candidate {n})."
    slug = f"salt-{major}-rc{n}-available"
    body = render_template("rc-intro-block", major=major, track=track, n=str(n))
    body += "\n" + render_template("installation-notes-simple")
    body += "\n" + render_template("reporting-issues-simple")

    front_matter = build_front_matter(
        draft=not args.publish,
        title=title,
        summary=summary,
        post_date=post_date,
        author="Salt Project Team",
        image="images/blog/new-release.png",
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
        release_notes_block = "\n".join(
            _security_release_notes_block(v, t) for v, t in zip(versions, tracks)
        )

    packages_list = "\n".join(f"- {v}" for v in versions)

    body = render_template(
        "security-body", summary=summary, release_notes_block=release_notes_block,
        packages_list=packages_list,
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
    return render_template("security-release-notes-block", version=version, track=track, major=major)


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
    body = render_template("announcement-body")
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
