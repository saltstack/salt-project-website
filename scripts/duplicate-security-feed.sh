#!/usr/bin/env bash
# Duplicate the security tag RSS feed to the legacy /security-announcements/
# URL so old subscribers (from before the tag-based RSS migration) keep
# getting the same feed content, byte-for-byte.
#
# Run this AFTER `hugo build` (or `hugo`), once the public/ directory has
# been generated, and BEFORE publishing/deploying it.
#
# Usage: scripts/duplicate-security-feed.sh [public_dir]
#   public_dir defaults to "public" relative to the repo root.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
public_dir="${1:-$repo_root/public}"

src="$public_dir/tags/security/index.xml"
dest_dir="$public_dir/security-announcements"
dest="$dest_dir/index.xml"

if [[ ! -f "$src" ]]; then
  echo "error: $src not found -- run 'hugo build' first" >&2
  exit 1
fi

mkdir -p "$dest_dir"
cp "$src" "$dest"
echo "Copied $src -> $dest"
