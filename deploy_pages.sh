#!/usr/bin/env bash
# Publish the built site (site/) to GitHub Pages. Does NOT build anything --
# run build_pages.py first.
#
# The site is committed to an orphan gh-pages branch of the repo and
# force-pushed, so it is idempotent. Pages is enabled on gh-pages / root.
#
# Usage:
#   python3 build_pages.py && ./deploy_pages.sh [site_dir]
#
# -> https://<user>.github.io/<repo>/
set -euo pipefail
cd "$(dirname "$0")"

GH_USER="jblowe"
REPO="gu-archive"
GIT_NAME="John B. Lowe"
GIT_EMAIL="johnblowe@gmail.com"

SITE="${1:-site}"
[ -f "$SITE/index.html" ] || {
  echo "error: $SITE/index.html not found -- run build_pages.py first" >&2
  exit 1
}
command -v gh  >/dev/null || { echo "error: gh CLI not found" >&2; exit 1; }
command -v git >/dev/null || { echo "error: git not found" >&2; exit 1; }

SITE_ABS="$(cd "$SITE" && pwd)"
REMOTE="https://github.com/$GH_USER/$REPO.git"

# publish via a throwaway orphan repo (single commit, force-pushed)
TMP="$(mktemp -d)"
echo "publishing $SITE_ABS -> $GH_USER/$REPO (gh-pages) ..."
(
  cd "$TMP"
  git init -q
  git checkout -q --orphan gh-pages
  cp -R "$SITE_ABS/." .
  touch .nojekyll
  git add -A
  git -c user.name="$GIT_NAME" -c user.email="$GIT_EMAIL" \
      commit -q -m "Publish $(date -u +%Y-%m-%dT%H:%MZ)"
  git push -f "$REMOTE" HEAD:gh-pages
)
rm -rf "$TMP"

# enable Pages on gh-pages / (no-op if already enabled)
gh api -X POST "repos/$GH_USER/$REPO/pages" \
   -f 'source[branch]=gh-pages' -f 'source[path]=/' >/dev/null 2>&1 || true

echo "deployed -> https://$GH_USER.github.io/$REPO/"
echo "(first deploy can take a minute or two to go live)"
