#!/usr/bin/env bash
# Update the vendored pydata-hugo-theme module: bumps it to the latest (or a
# pinned) version, re-vendors it into _vendor/, and re-copies the attribution
# files (LICENSE/README.md) that `hugo mod vendor` doesn't carry over.
#
# Usage: scripts/update-vendored-theme.sh [version]
#   version defaults to latest (`hugo mod get -u`); pass e.g. "v0.2.0" to pin.
#
# Requires Go and Hugo (extended) on PATH. This is a maintenance-only
# operation -- regular `hugo build`/`hugo server` need neither.
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

echo "==> Vendoring"
hugo mod vendor

echo "==> Re-copying LICENSE/README.md (hugo mod vendor skips non-Hugo files)"
# `go list -m` needs the module in Go's own module cache, which Hugo's
# internal module client doesn't necessarily populate -- fetch it
# explicitly first.
go mod download "$MODULE_PATH"
module_dir="$(go list -m -f '{{.Dir}}' "$MODULE_PATH")"
vendor_dir="_vendor/${MODULE_PATH}"
cp "$module_dir/LICENSE" "$vendor_dir/LICENSE"
cp "$module_dir/README.md" "$vendor_dir/README.md"

echo "==> Done. Review the diff, then commit, e.g.:"
echo "    git add go.mod go.sum _vendor"
echo "    git commit -m 'chore(theme): update pydata-hugo-theme module'"
