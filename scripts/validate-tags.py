#!/usr/bin/env python3
"""
Validate that every blog post uses only the approved tag taxonomy.

Approved tags are defined in scripts/tags.toml — edit that file to add
or remove tags from the taxonomy.

Exit code: 0 if all posts are clean, 1 if any violations are found.
Usage: python3 scripts/validate-tags.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _blog_common import load_approved_tags  # noqa: E402

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")

SKIP_FILES = {"_index.md"}


def parse_tags(content: str) -> list[str]:
    m = re.search(r'^tags:\s*\n((?:[ \t]+-[^\n]*\n?)+)', content, re.MULTILINE)
    if not m:
        return []
    tags = []
    for line in m.group(1).splitlines():
        tag = line.strip().lstrip("- ").strip().strip('"').strip("'")
        if tag:
            tags.append(tag)
    return tags


def main() -> int:
    approved_tags = load_approved_tags()

    blog_dir = os.path.abspath(BLOG_DIR)
    if not os.path.isdir(blog_dir):
        print(f"ERROR: blog directory not found: {blog_dir}", file=sys.stderr)
        return 1

    files = sorted(
        f for f in os.listdir(blog_dir)
        if f.endswith(".md") and f not in SKIP_FILES
    )

    violations: list[tuple[str, list[str]]] = []
    no_tags: list[str] = []

    for fname in files:
        path = os.path.join(blog_dir, fname)
        with open(path, encoding="utf-8") as f:
            content = f.read()

        tags = parse_tags(content)

        if not tags:
            no_tags.append(fname)
            continue

        bad = [t for t in tags if t not in approved_tags]
        if bad:
            violations.append((fname, bad))

    # Report
    ok = not violations and not no_tags

    if violations:
        print(f"FAIL — {len(violations)} post(s) with unapproved tags:\n")
        for fname, bad_tags in violations:
            print(f"  {fname}")
            for t in bad_tags:
                print(f"    ✗  '{t}'  (not in approved set)")
        print()

    if no_tags:
        print(f"FAIL — {len(no_tags)} post(s) with no tags (at least one required):\n")
        for fname in no_tags:
            print(f"  {fname}")
        print()

    total = len(files)
    clean = total - len(violations) - len(no_tags)

    if ok:
        print(f"OK — all {total} posts use approved tags only.")
        print(f"\nApproved tags: {', '.join(sorted(approved_tags))}")
    else:
        print(f"Summary: {clean}/{total} posts clean, "
              f"{len(violations)} unapproved tag(s), {len(no_tags)} missing tags.")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
