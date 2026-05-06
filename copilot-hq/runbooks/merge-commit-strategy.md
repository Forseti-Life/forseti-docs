# Merge/Commit Strategy — Complex Multi-Team Repo

**Owner:** `ceo-copilot-2`  
**Effective Date:** 2026-04-23  
**Last Updated:** 2026-04-23  
**Authority:** Org-wide + CEO (applies to all merges in this repo and all coordinated product repos)

---

## Executive Summary

This repo (`keithaumiller/forseti.life`) is a **unified monorepo with coordinated submodules plus explicitly decoupled product checkouts**, containing:
- **Coordinated Git submodules** for shared platform repos
- **Standalone product checkouts** where independent product history is intentional
- **3 independent push clones** in `/root/` (not coordinated)
- **Multiple concurrent teams** (pm-forseti, qa-forseti, dev-forseti, pm-dungeoncrawler, pm-infra, etc.)
- **Multi-layered instructions** (org-wide → role → site → seat)
- **Audit-trail sessions/** directory (append-only log of all agent work)
- **Runtime state** that should never be committed (PIDs, locks, transient artifacts)

This document defines the **authoritative merge/commit strategy** to keep this structure healthy and prevent:
- Silent data loss (sessions/ files deleted in bad merges)
- Cross-team conflicts (concurrent editing of the same files)
- Runtime state pollution (PIDs and ephemeral data committed to the repo)
- Orphaned work items (teams merging changes that break the upstream pipeline)

---

## Guiding Principles

### 1. Sessions are Append-Only Audit Trail
- `sessions/` directory contains the complete history of every agent's work (inbox, outbox, artifacts).
- **MUST be fully tracked** in version control (per `/runbooks/git-management.md`).
- Each commit should **preserve all sessions/ history** — no files should be deleted by a merge.
- When a merge deletes sessions/ files, treat it as a **CRITICAL data loss event** → restore from backup.

### 2. Single Main Branch (Production = Master)
- **One production branch:** `main`
- **Remote:** `origin/main` (GitHub Forseti-Life org)
- **All releases pushed to:** `main`
- **Feature branches:** permitted only for dev-laptop work (see section on Dev Worker Protocol).
- **No long-lived feature branches.** Branches merge back to `main` within 1 release cycle.

### 3. Team Separation by Website Scope
- Each team owns a website (forseti.life, dungeoncrawler, infrastructure, etc.).
- Teams edit files within their **owned scope** (defined in `org-chart/agents/instructions/`).
- **Cross-scope edits require passthrough requests** (see `runbooks/coordination-policy.md`).
- Merge conflicts are **rare** if scopes are enforced correctly.

### 4. Coordinated Pushes (Not Frequent Merges)
- Changes are **grouped into release windows**, not pushed individually.
- **Release Coordinator** (`pm-forseti` by default) performs the coordinated push once all gates pass.
- Push = single atomic commit that includes all teams' changes for that cycle.
- Between pushes, work stays in `sessions/` as inbox/outbox items; code changes are committed but **not pushed**.

### 5. Runtime State Isolation
- Runtime state (PIDs, locks, transient logs) is **NEVER committed** (see `.gitignore`).
- If runtime state appears in a commit, the issue must be fixed **immediately** before the next merge.

---

## Commit Rules (For All Seats)

### Rule 1: Who Can Commit?
- **CEO (ceo-copilot-2):** full authority, commits on behalf of teams, coordinates releases.
- **Dev seats (dev-forseti, dev-dungeoncrawler, dev-infra):** commits within owned code scope.
- **All other seats:** **do not commit directly**. Create inbox items or escalate to CEO if code changes needed.

### Rule 2: Commit Message Format (Required)
Every commit must include:
1. **Subject** (1 line, ~50 chars): present tense, descriptive action
2. **Body** (paragraph): why this change, what it affects
3. **Co-authored-by trailer** (REQUIRED for CEO commits):
   ```
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
   ```

**Example (good):**
```
Fix: Ignore all runtime .pid files (orchestrator, dev-sync)

Added .*-loop.pid pattern to .gitignore to catch all daemon pids.
Removed .orchestrator-loop.pid and .dev-sync-loop.pid from git tracking
since they are ephemeral runtime state, never production config.

Fixes merge health issue where PIDs were being committed at every 
orchestrator tick, causing unnecessary merge conflicts.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

### Rule 3: What Can Be Committed?
✅ **OK to commit:**
- Source code (modules, themes, scripts)
- Configuration (Drupal config/sync, runbooks, instructions)
- Artifacts (session inbox/outbox/artifacts as part of audit trail)
- Lesson learned documents (knowledgebase/)
- Project/release metadata (dashboards/, features/)

❌ **MUST NOT commit:**
- Runtime PIDs (`.*.pid`, `.*-loop.pid` — see `.gitignore`)
- Transient locks (`.exec-lock/**`, `tmp/.agent-exec-*.lock`)
- Local Copilot logs (`**/events.jsonl`, `**/workspace.yaml`)
- Volatile symlinks (`sessions/**/artifacts/**/latest`)
- Generated artifacts (LLM cache, model weights, venv/)

### Rule 4: Commit Scope (Keep Commits Focused)
- **One logical unit per commit** (one feature, one bug fix, one config update).
- **Avoid mega-commits** that mix multiple unrelated changes.
- **Atomic commits** (either all pass or all fail — no partial states).
- **Link to release cycle** when applicable:
  ```
  Feature: forseti-langgraph-console-admin (release: 20260412-forseti-release-q)
  ```

### Rule 5: Checkpoint Commits for Session State
- When CEO finishes a significant phase, create a **checkpoint commit** to persist session state.
- Format:
  ```
  Checkpoint: <phase-name> — <description>

  <Summary of what was processed/decided>

  Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
  ```

**Example:**
```
Checkpoint: Phase 1 Orient — orchestrator restarted, merge health fixed

- Restarted orchestrator (was dead, PID stale)
- Fixed .gitignore to ignore .*-loop.pid files
- Removed incorrectly-tracked .orchestrator-loop.pid
- Cleared 87 tracked changes via checkpoint commit

Ready to proceed with Phase 2 (unblock shipping pipeline).

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

---

## Submodule Merge Rules (20-Submodule Model)

### Overview: Merged Submodules, Not Merged Code

The unified monorepo uses **Git submodules** to track all 20 product repos. When merging:
- **Main repo .gitmodules** is what gets merged (metadata about submodule pointers)
- **Individual submodules** remain independent repos (they don't merge via the main repo)
- Each submodule has its own branch protection rules and CI/CD

### Rule: Pre-Merge Submodule Verification

Before merging the main repo, verify all 20 submodules are healthy:

```bash
# Show all 20 submodules and their current commits
git submodule status

# Expected output shows all 20 repos at specific commits (no +/- prefixes)
# +<sha> = has uncommitted changes (usually means local dev work)
# -<sha> = submodule not yet initialized
# U<sha> = merge conflict in submodule pointer
```

If any submodule shows `U` (merge conflict):
```bash
# Use the owning team's version
git checkout --theirs <submodule-path>
git add <submodule-path>
git commit -m "resolve: use <owning-team> version for <submodule> per coordination-policy"
```

### Rule: .gitmodules Merge Conflicts

If `.gitmodules` has merge conflicts (two teams added submodules):
1. **Review both sides** to ensure no duplicate entries
2. **Keep both** new submodule entries (each team owns theirs)
3. **Commit merge resolution** with explanation

Example:
```bash
# After resolving conflict in .gitmodules
git add .gitmodules
git commit -m "resolve: merge .gitmodules from two teams' submodule additions"
```

### Rule: Backup All 20 Submodules on Merge

The `workspace-merge-safe.sh` script automatically:
1. **Backs up all 20 submodules** (via tar in `/tmp/workspace-merge-backup-<ts>/`)
2. **Records all current submodule pointers** in backup manifest
3. **Post-merge: verifies no submodule pointers were silently deleted**

This prevents accidental loss of submodule references.

---

## Merge Rules (When Pulling From GitHub or Merging Branches)

### Rule 1: Pre-Merge Safety Gate (REQUIRED)

**Before merging anything**, run:
```bash
./scripts/workspace-merge-safe.sh --dry-run
```

This:
1. Creates timestamped backup of `sessions/` to `/tmp/workspace-merge-backup-<ts>/`
2. Records all current inbox/outbox paths in the backup manifest
3. **Does NOT execute the merge** (just analysis + backup)
4. Reports any unprocessed inbox items

**Exit codes:**
- `0` = backup successful, merge is safe to proceed
- `1` = backup failed (do not proceed)
- `2` = backup successful but unprocessed items detected (proceed with caution, document decision)

### Rule 2: Execute the Merge (Use the Safe Script)

**Never use bare `git merge`.**

Instead:
```bash
./scripts/workspace-merge-safe.sh <branch-or-commit>
```

This:
1. Creates timestamped backup (same as dry-run)
2. Executes: `git merge --no-edit <branch-or-commit>`
3. Post-merge: compares `sessions/` against pre-merge state
4. **If files were deleted:** warns with restoration command

**Exit codes:**
- `0` = merge succeeded, no data loss
- `1` = merge failed (backup preserved, safe to abort)
- `2` = merge succeeded but `sessions/` files were deleted (WARNING — **RESTORE IMMEDIATELY**)

### Rule 3: If Sessions Files Were Deleted (Exit Code 2)

Restore immediately:
```bash
cp -r /tmp/workspace-merge-backup-<ts>/sessions/ .
git add -f sessions/ && git commit -m "restore: recover sessions/ files lost in workspace merge"
```

**Never ignore this warning.** Deleted sessions/ files represent lost work, escalations, and audit trail.

### Rule 4: Resolve Merge Conflicts (By Scope Ownership)

If a merge conflict occurs:
1. **Identify the conflicting file.**
2. **Map to owner** using `org-chart/agents/instructions/` and `org-chart/ownership/`.
3. **Resolve by scope ownership:**
   - If both sides edited the same module/file → **escalate to owning PM/Dev** for decision.
   - If one side is runtime state (PIDs, logs) → **take the non-runtime version**.
   - If one side is sessions/ content → **take both versions** (append, don't delete).

**Example resolution:**
```
# Conflicted file: org-chart/sites/forseti.life/site.instructions.md
# Owner: pm-forseti
# Decision: Contact pm-forseti for the correct version
git checkout --theirs org-chart/sites/forseti.life/site.instructions.md
git add org-chart/sites/forseti.life/site.instructions.md
git commit -m "resolve: use pm-forseti version for site.instructions.md per scope ownership"
```

### Rule 5: Post-Merge Verification

After a successful merge:
```bash
# Verify no broken symlinks
find sessions/ -type l -exec test ! -e {} \; -print

# Verify git status is clean (except for expected gitignored files)
git status

# Verify no orphaned .inwork markers (interrupt recovery)
find sessions/ -name ".inwork" | wc -l

# Optional: verify orchestrator can start
python3 orchestrator/run.py --once --no-publish --dry-run
```

---

## Push Rules (For Coordinated Releases)

### Rule 1: Who Pushes?
- **Release Coordinator** (default: `pm-forseti`) performs the coordinated push.
- **Only when:** all release gates (R0–R6) are satisfied (see `runbooks/coordinated-release.md`).
- **Script:** `scripts/post-coordinated-push.sh` (CEO executes this on behalf of PM if PM delegates).

### Rule 2: Push Verification (Pre-Push Checklist)

Before pushing:
```bash
# Verify all release gates
./scripts/release-signoff-status.sh <release-id>
# Expected: "all signatories present"

# Verify no untracked files (except gitignored)
git status --short

# Verify merge history (no unresolved MERGE_HEAD)
git status | grep -i merge || echo "✅ No merge conflicts"

# Verify recent commits look correct
git log --oneline -10
```

### Rule 3: Push Command (GitHub)

```bash
# Verify local branch is main
git branch | grep "^\* main"

# Verify remote is GitHub Forseti-Life org
git remote -v | grep github.com/Forseti-Life/

# Push to origin/main
git push origin main
```

**Note:** PAT token is stored in `/home/ubuntu/github.token` (CEO access only).

### Rule 4: Post-Push Actions

After push:
1. **Verify GitHub** received the commit:
   ```bash
   git log --oneline origin/main -1
   ```
2. **Verify GitHub Actions** triggered (deploy.yml, any other workflows).
3. **Wait for workflow completion** before declaring release complete.
4. **Run post-release QA** (Gate R5): `ALLOW_PROD_QA=1 bash scripts/site-audit-run.sh forseti`
5. **Update next_release_id** via `scripts/post-coordinated-push.sh`.

---

## Conflict Scenarios & Resolution

### Scenario 1: Two Teams Edited the Same File
**Example:** Both `pm-forseti` and `pm-dungeoncrawler` edited `org-chart/kpis.md`

**Resolution:**
1. Run `git diff --ours --theirs org-chart/kpis.md` to see both versions.
2. Manually merge (copy both additions, remove duplicates).
3. Commit: `git add org-chart/kpis.md && git commit -m "merge: combine KPI updates from both teams"`

### Scenario 2: Runtime State (PIDs) Got Committed
**Example:** `.orchestrator-loop.pid` appears in a commit

**Resolution:**
1. Check `.gitignore` — ensure `.*-loop.pid` is listed.
2. If not: update `.gitignore` (add pattern).
3. Remove file from tracking: `git rm --cached .orchestrator-loop.pid`.
4. Commit: `git commit -m "fix: remove .orchestrator-loop.pid from tracking, already gitignored"`
5. Verify: `git check-ignore .orchestrator-loop.pid` should return `0` (ignored).

### Scenario 3: Sessions/ Files Deleted by Merge
**Example:** Merge command deleted 10 sessions/ files

**Resolution:**
1. Merge command exited with code `2` (detected by `workspace-merge-safe.sh`).
2. **Restore immediately** from backup (see Rule 3 above).
3. Commit the restoration.
4. **Investigate root cause**: why were sessions/ files deleted? (usually: one side deleted, other side modified — git can't merge auto-merge).
5. **Document** in the restoration commit message and in a KB lesson.

### Scenario 4: Orphaned Inbox Items After Merge
**Example:** A team's inbox items are no longer referenced after a merge

**Resolution:**
1. CEO runs `./scripts/hq-blockers.sh` to find orphaned items.
2. For each orphaned item: check if corresponding outbox exists.
3. If outbox exists: mark item done (stale inbox marker).
4. If no outbox and item is > 48h old: escalate to owning team (may be dead-letter).

---

## .gitignore Rules (Authoritative)

These patterns **must** be in `.gitignore` to keep the repo clean:

```gitignore
# Never commit raw local Copilot session logs
**/events.jsonl
**/workspace.yaml
**/checkpoints/

# Common local artifacts
.DS_Store
*.log
*.tmp

# Runtime state (ephemeral)
tmp/escalation-streaks/
tmp/site-audit/
tmp/.last-publish-agent-tracker.epoch
tmp/org-control.json

# Runtime locks
**/.exec-lock/
tmp/.agent-exec-*.lock
tmp/.agent-exec-*/

# Python bytecode
**/__pycache__/

# Local LLM (models, cache, venv)
llm/models/*.gguf
llm/models/*.bin
llm/cache/sessions/
llm/.venv/

# CEO loop / daemon runtime PIDs (all -loop.pid patterns)
.*-loop.pid
.orchestrator-loop.pid
.dev-sync-loop.pid
inbox/responses/.ceo-health-last-queue

# Session volatile pointers (symlinks, latest markers)
sessions/**/artifacts/**/latest
sessions/**/artifacts/**/latest.*
```

**Enforcement:**
- When adding new runtime files, update `.gitignore` **immediately**.
- Verify with: `git check-ignore <filename>` (should return 0 for ignored files).
- If file is tracked but should be ignored: `git rm --cached <filename>` and recommit the `.gitignore` change.

---

## Release Workflow (Commit → Merge → Push)

### Phase 1: Development (Weeks 1–2 of release cycle)
```
dev-* commits code changes to main (or local branch if dev-laptop)
↓
git add / git commit -m "feat: <feature> (release: <id>)"
↓
Changes stay local (not pushed yet)
↓
Sessions/ updated with dev work items (inbox/outbox/artifacts)
```

### Phase 2: Testing & Verification (Week 2–3)
```
qa-* runs test suites (local or production)
↓
QA outbox produced with APPROVE/BLOCK evidence
↓
Sessions/ updated with qa work items
```

### Phase 3: Sign-Off (End of week 3)
```
pm-* verifies all gates (R0–R6)
↓
pm-forseti or pm-dungeoncrawler signs off via scripts/release-signoff.sh
↓
Sessions/ updated with pm signoff artifacts
```

### Phase 4: Coordinated Push (Release day)
```
Release Coordinator verifies: ./scripts/release-signoff-status.sh <id>
↓
git push origin main (single atomic commit with all teams' changes)
↓
Verify GitHub Actions triggered
↓
Wait for deploy workflows to complete
↓
Run post-release QA (Gate R5)
↓
Advance release: scripts/post-coordinated-push.sh
```

---

## Instruction Stack (How Merges Respect Scopes)

Each merge is **scoped by instruction layer**:

1. **Org-wide** (`org-chart/org-wide.instructions.md`): applies to all merges
2. **Role** (`org-chart/roles/ceo.instructions.md`): applies to CEO merge decisions
3. **Site** (`org-chart/sites/forseti.life/site.instructions.md`): applies to forseti-specific merges
4. **Seat** (`org-chart/agents/instructions/ceo-copilot-2.instructions.md`): applies to this CEO seat's merge authority

**Merge authority by layer:**
- **Org-wide:** no bare `git merge`; use `workspace-merge-safe.sh`
- **Role:** CEO coordinates all merges; other roles don't merge
- **Site:** forseti merges only forseti-scoped files (unless passthrough)
- **Seat:** ceo-copilot-2 can merge anything; other seats must escalate

---

## Audit & Compliance

### Weekly Merge Audit
CEO runs (part of Phase 1 Orient):
```bash
git log --oneline main -20 | grep -i "merge\|checkpoint\|fix"
git status
./scripts/workspace-merge-safe.sh --dry-run
```

### Quarterly Merge Strategy Review
- Check if `.gitignore` needs updates.
- Review any merge conflicts from the past 3 months.
- Update this document if patterns or rules have changed.
- File KB lesson if a new conflict pattern emerges.

### Post-Incident: Merge Failure Root Cause
If a merge fails or loses data:
1. Document the failure in a KB lesson.
2. Update `.gitignore` or merge script if needed.
3. Add test case to prevent recurrence.
4. Escalate to Board if systemic (e.g., "merge script is broken").

---

## References

- **Git management audit trail:** `runbooks/git-management.md`
- **Coordinated release process:** `runbooks/coordinated-release.md`
- **Orchestration (merges in automation context):** `runbooks/orchestration.md`
- **Coordination policy (cross-team scope):** `runbooks/coordination-policy.md`
- **Workspace merge script:** `scripts/workspace-merge-safe.sh`
- **Release signoff status:** `scripts/release-signoff-status.sh`
- **Post-coordinated push:** `scripts/post-coordinated-push.sh`

---

## Revision History

| Date | Author | Change |
|---|---|---|
| 2026-04-23 | ceo-copilot-2 | Initial audit & documentation (v1.0) — formalized merge/commit strategy, added pre-merge safety gate, documented conflict scenarios, updated .gitignore rules |
