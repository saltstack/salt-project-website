#!/usr/bin/env bash
# Update the vendored pydata-hugo-theme module: bumps it to the latest (or a
# pinned) version, re-vendors it into _vendor/, and re-copies the attribution
# files (LICENSE/README.md) that `hugo mod vendor` doesn't carry over.
#
# Usage: scripts/update-vendored-theme.sh [version]
#   version defaults to latest (`hugo mod get -u`); pass e.g. "v0.2.0" to pin.
#
# Requires Go, Hugo (extended), and Node/npm on PATH. This is a
# maintenance-only operation -- regular `hugo build`/`hugo server` need
# none of them, since they build from the already-vendored _vendor/.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

MODULE_PATH="github.com/saltstack/pydata-hugo-theme"
version="${1:-}"

if grep -qE "^\s*replace\s+${MODULE_PATH//\//\\/}\s*=>" go.mod; then
  echo "warning: go.mod has a local 'replace' for $MODULE_PATH -- hugo mod get -u" >&2
  echo "         is a no-op while that's in place; vendoring will just re-copy" >&2
  echo "         from the local replace path." >&2
fi

if [[ -n "$version" ]]; then
  echo "==> Pinning $MODULE_PATH@$version"
  hugo mod get "${MODULE_PATH}@${version}"
else
  echo "==> Updating $MODULE_PATH to latest"
  hugo mod get -u "$MODULE_PATH"
fi

# Hugo maintains its own module cache, separate from Go's (`go list -m`
# reports a different, unrelated copy under GOMODCACHE) -- resolve the
# version Hugo actually pinned, then compute its own on-disk cache path
# directly, so we can `npm ci` the theme's build-time deps into the exact
# copy `hugo mod vendor` will read from. Without this, vendoring fails on
# a cold cache (no local copy of the theme with node_modules already
# installed lying around) -- e.g. any first vendor of a new version, or
# any CI run, since CI runners are always cold.
resolved_version="$(hugo mod graph --ignoreVendorPaths '**' | awk -v mod="$MODULE_PATH@" '$2 ~ "^"mod {sub(mod, "", $2); print $2}')"
if [[ -z "$resolved_version" ]]; then
  echo "error: could not determine the resolved version of $MODULE_PATH from 'hugo mod graph'" >&2
  exit 1
fi
hugo_cache_dir="${HUGO_CACHEDIR:-${XDG_CACHE_HOME:-$HOME/.cache}/hugo_cache}"
module_dir="${hugo_cache_dir}/modules/filecache/modules/pkg/mod/${MODULE_PATH}@${resolved_version}"

if [[ -f "$module_dir/package.json" ]]; then
  echo "==> Installing the theme's build-time npm deps (needed for its"
  echo "    [[module.mounts]] before vendoring can find them)"
  ( cd "$module_dir" && npm ci )
fi

echo "==> Vendoring"
hugo mod vendor

# `hugo mod get`/`hugo mod vendor` don't prune go.sum the way a plain `go
# mod tidy` does for a normal buildable module -- old versions' checksums
# just accumulate across bumps. A bare `go mod tidy` isn't safe here either
# (this repo has no .go source files, so it tries to resolve importable Go
# packages across the whole tree instead of just tidying go.sum), so prune
# by hand: drop any line for this module that isn't the version we just
# resolved.
if [[ -f go.sum ]]; then
  awk -v mod="$MODULE_PATH" -v ver="$resolved_version" \
    '$1 != mod || $2 == ver || $2 == ver"/go.mod" { print }' \
    go.sum > go.sum.tmp && mv go.sum.tmp go.sum
fi

echo "==> Re-copying LICENSE/README.md (hugo mod vendor skips non-Hugo files)"
vendor_dir="_vendor/${MODULE_PATH}"
cp "$module_dir/LICENSE" "$vendor_dir/LICENSE"
cp "$module_dir/README.md" "$vendor_dir/README.md"

echo "==> Done. Review the diff, then commit, e.g.:"
echo "    git add go.mod go.sum _vendor"
echo "    git commit -m 'chore(theme): update pydata-hugo-theme module'"
