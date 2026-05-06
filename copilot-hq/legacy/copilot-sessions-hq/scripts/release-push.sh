#!/usr/bin/env bash
# release-push.sh
# Commit and push all modified repositories at release time.
# Called by the orchestrator's coordinated_push_step before triggering deploy.
#
# Usage: bash scripts/release-push.sh <release-id>
# Exit codes:
#   0 — all dirty repos committed and pushed (or already clean)
#   1 — at least one repo failed to push
#
# Applies the same safety guards as auto-checkpoint.sh (denylist, too-many-changes)
# but uses a release-tagged commit message and exits non-zero on push failure.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

RELEASE_ID="${1:-release}"
ISO="$(date -Iseconds)"
COMMIT_MSG="release: ${RELEASE_ID} @ ${ISO}"

REPOS=(
  "/home/ubuntu/forseti.life"
  "/home/ubuntu/copilot-sessions-hq"
)

# Branch to push for each repo (key=repo path, value=branch)
declare -A REPO_BRANCH
REPO_BRANCH["/home/ubuntu/forseti.life"]="main"
REPO_BRANCH["/home/ubuntu/copilot-sessions-hq"]="master"

PUSH_FAILED=0

is_dirty() {
  git --no-pager status --porcelain=v1 | grep -q .
}

denylist_present() {
  git --no-pager status --porcelain=v1 | awk '{print $2}' \
    | grep -E -q '(^|/)(settings\.php|settings\.local\.php|services\.local\.yml)$|(^|/)\.env($|\.)|\.(pem|key)$'
}

too_many_changes() {
  local n
  n="$(git --no-pager status --porcelain=v1 | wc -l | awk '{print $1}')"
  local max="${AUTO_CHECKPOINT_MAX_CHANGES:-5000}"
  [ "$n" -gt "$max" ]
}

for repo in "${REPOS[@]}"; do
  if [ ! -d "${repo}/.git" ]; then
    echo "[release-push] SKIP (not a git repo): ${repo}"
    continue
  fi

  cd "${repo}"
  branch="${REPO_BRANCH[$repo]:-main}"

  if ! is_dirty; then
    echo "[release-push] CLEAN: ${repo}"
    continue
  fi

  if denylist_present; then
    echo "[release-push] BLOCKED (denylist match — secrets guard): ${repo}" >&2
    PUSH_FAILED=1
    continue
  fi

  if too_many_changes; then
    echo "[release-push] BLOCKED (too many changes): ${repo}" >&2
    PUSH_FAILED=1
    continue
  fi

  git add -A

  if git diff --cached --quiet; then
    echo "[release-push] CLEAN (after add): ${repo}"
    continue
  fi

  git commit -q \
    -m "${COMMIT_MSG}" \
    -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

  if git push -q origin "${branch}"; then
    echo "[release-push] PUSHED: ${repo} -> ${branch}"
  else
    echo "[release-push] PUSH FAILED: ${repo} -> ${branch}" >&2
    PUSH_FAILED=1
  fi
done

if [ "${PUSH_FAILED}" -ne 0 ]; then
  echo "[release-push] ERROR: one or more repos failed to push" >&2
  exit 1
fi

echo "[release-push] done: all repos committed and pushed for ${RELEASE_ID}"
exit 0
