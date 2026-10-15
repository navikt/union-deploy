#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

tag=v2

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Commit or remove worktree changes before releasing $tag." >&2
  exit 1
fi

if remote_tag="$(git ls-remote --exit-code --refs origin "refs/tags/$tag")"; then
  old_oid="${remote_tag%%$'\t'*}"
else
  status=$?
  if [[ "$status" -ne 2 ]]; then
    echo "Cannot query $tag on origin; refusing to release." >&2
    exit 1
  fi
  # An empty expected OID only permits creation if the remote tag is still absent.
  old_oid=""
fi
commit="$(git rev-parse HEAD)"

git push --force-with-lease="refs/tags/$tag:$old_oid" origin "$commit:refs/tags/$tag"
git tag -f "$tag" "$commit"

echo "Released $tag at $commit."
