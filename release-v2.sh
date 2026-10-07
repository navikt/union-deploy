#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

tag=v2

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Commit or remove worktree changes before releasing $tag." >&2
  exit 1
fi

remote_tag="$(git ls-remote --exit-code --refs origin "refs/tags/$tag")" || {
  echo "Cannot find $tag on origin; refusing to create a new release tag." >&2
  exit 1
}
old_oid="${remote_tag%%$'\t'*}"
commit="$(git rev-parse HEAD)"

git push --force-with-lease="refs/tags/$tag:$old_oid" origin "$commit:refs/tags/$tag"
git tag -f "$tag" "$commit"

echo "Released $tag at $commit."
