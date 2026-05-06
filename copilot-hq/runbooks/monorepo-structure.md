# Monorepo Architecture: Unified Submodule Model

**Last Updated:** 2026-04-23  
**Author:** CEO/Orchestration  
**Status:** Active  
**Review Cycle:** Quarterly

---

## Overview

Forseti.Life operates as a **unified monorepo with coordinated submodules** plus a small set of independent product checkouts and push clones. This document describes the architecture, rationale, and operational procedures.

**Key Principle:** Shared platform repos are version-locked in the main repository where appropriate, while explicitly decoupled product repos can operate on their own release cadence when that better fits production ownership.

---

## Architecture

### Main Repository Structure

```
/home/ubuntu/forseti.life/
├── .git/                          (Shared root for copilot-hq tracked content)
├── .gitmodules                    (Tracks coordinated submodules owned by copilot-hq)
├── copilot-hq/                    (Control plane: orchestration, releases, governance)
│   ├── orchestrator/              (Release automation, agent dispatch)
│   ├── org-chart/                 (Instructions, org structure, decision matrix)
│   └── sessions/                  (Session state, artifacts, inbox/outbox)
│
├── ─────── INDEPENDENT PRODUCT CHECKOUTS ───────
├── dungeoncrawler-pf2e/           (Standalone PF2E product repo checkout; not tracked as a copilot-hq submodule)
│
├── ─────── EXISTING SUBMODULES ───────
├── dungeoncrawler-content/        (Shared content; symlinked in /root/)
├── forseti-shared-modules/        (Shared utilities, common functions)
├── forseti-devops/                (Infrastructure, deployment, scripts)
├── forseti-meshd/                 (Mesh networking service)
├── forseti-mobile/                (Mobile app code)
├── forseti-docs/                  (Public documentation site)
├── forseti-platform-specs/        (API specs, standards, design docs)
├── forseti-job-hunter/            (Job Hunter product)
└── h3-geolocation/                (Geolocation utility library)
│
└── ─────── NEW SUBMODULES (10) ───────
    ├── forseti-safety-content/    (Safety content library)
    ├── forseti-safety-calculator/ (Safety calculation engine)
    ├── forseti-content/           (General content repository)
    ├── forseti-community-incident-report/  (Community incident tracking)
    ├── forseti-company-research/  (Research & analysis)
    ├── forseti-nfr/               (Non-functional requirements docs)
    ├── forseti-copilot-agent-tracker/     (Agent lifecycle tracking)
    ├── forseti-institutional-management/  (Institutional governance)
    ├── forseti-jobhunter-tester/ (QA/testing for Job Hunter)
    └── forseti-agent-evaluation/  (Agent evaluation framework)
```

### Independent Push Clones (in /root/)

```
/root/
├── ai-conversation-push/          (Autonomous AI conversation engine)
├── dungeoncrawler-tester-push/    (DungeonCrawler QA utilities)
├── forseti-cluster-push/          (Cluster infrastructure utilities)
└── dungeoncrawler-content-push → SYMLINK to submodule
```

---

## Rationale: Why Submodules?

### Coordinated Releases (R1-R4)

All 20 product submodules are version-locked in a single atomic commit. When an R1-R4 release cycle executes:
- The main repo commits one sha that pins all 20 submodules to specific commits
- Every consumer gets the exact same versions of all dependencies
- No version skew, no partial deployments, no broken cross-dependencies

### Unified Git History

Single shared `.git` root means:
- One authoritative version history for the entire platform
- Merge conflicts resolved once, not 20 times
- Release notes tell the story of all products together
- Easy rollback: revert single commit rolls back all 20 repos

### Simplified Governance

All repos live in one namespace:
- Single `.gitmodules` file = single source of truth
- One set of branch protection rules
- One set of CI/CD triggers
- Easier to audit cross-repo changes

### Independence Without Duplication

Each submodule has its own `.git` directory but shares the parent's git management:
- Teams can work on submodules independently
- No need to maintain separate CI/CD pipelines
- No duplicate code
- Easy to trace dependencies

---

## Operational Model

### DungeonCrawler host layout

On this host, the live DungeonCrawler site is served from:

```bash
/var/www/html/dungeoncrawler/web
```

The live docroot symlinks these paths back into the main repo:

```bash
/var/www/html/dungeoncrawler/web/modules/custom -> /home/ubuntu/forseti.life/sites/dungeoncrawler/web/modules/custom
/var/www/html/dungeoncrawler/web/themes/custom  -> /home/ubuntu/forseti.life/sites/dungeoncrawler/web/themes/custom
/var/www/html/dungeoncrawler/config/sync        -> /home/ubuntu/forseti.life/sites/dungeoncrawler/config/sync
```

Operational implication:
- `dungeoncrawler-pf2e` is the canonical editable product repo for Dungeoncrawler-owned code.
- `sites/dungeoncrawler` remains a compatibility bridge inside the main repo.
- The current delegated Dungeoncrawler site paths in `sites/dungeoncrawler` resolve into `dungeoncrawler-pf2e` via symlinked custom-module/theme/config paths.

### For Developers

```bash
# Clone entire monorepo with all 20 submodules
git clone --recurse-submodules https://github.com/Forseti-Life/forseti.life.git

# Work on a specific submodule
cd forseti-job-hunter
# Make changes, test, commit (commits go to submodule repo)
git commit -m "feat: add new feature"
git push

# Back in main repo, update the submodule pointer
cd ..
git add forseti-job-hunter
git commit -m "chore: Update forseti-job-hunter to latest"
git push
```

### For Release Cycle

```bash
# R1: Verify all submodules at desired commits
git submodule foreach 'git log -1 --oneline'

# R2: Test all submodules together
./ workspace-merge-safe.sh --test  # backs up all 20, runs tests, restores

# R3: Create release commit (pins all 20)
git commit -m "Release: R1-2026-04-23 - All 20 submodules coordinated"

# R4: Deploy all 20 repos simultaneously
```

### For Merge Safety

Before any merge into main:
1. `workspace-merge-safe.sh` backs up all 20 submodules
2. Merge proceeds
3. If merge succeeds but deletions occurred (exit code 2):
   - Sessions/ files were auto-deleted (expected)
   - Production ready
4. If merge fails, all 20 repos automatically restored

---

## The 20 Submodules: Ownership & Purpose

| Submodule | Product Team | Purpose | Status |
|-----------|--------------|---------|--------|
| dungeoncrawler-pf2e | pm-dungeoncrawler | PF2E content & engine | ✅ Active |
| dungeoncrawler-content | pm-dungeoncrawler | Shared content | ✅ Active |
| forseti-shared-modules | pm-forseti | Shared utilities | ✅ Active |
| forseti-devops | pm-infra | Infrastructure & deployment | ✅ Active |
| forseti-meshd | pm-forseti | Mesh networking | ✅ Active |
| forseti-mobile | pm-forseti | Mobile app | ✅ Active |
| forseti-docs | pm-forseti | Public documentation | ✅ Active |
| forseti-platform-specs | pm-forseti | API specs & standards | ✅ Active |
| forseti-job-hunter | pm-forseti | Job Hunter product | ✅ Active |
| h3-geolocation | pm-forseti | Geolocation utility | ✅ Active |
| forseti-safety-content | pm-forseti | Safety content library | ✅ New (Phase 2) |
| forseti-safety-calculator | pm-forseti | Safety calculations | ✅ New (Phase 2) |
| forseti-content | pm-forseti | General content | ✅ New (Phase 2) |
| forseti-community-incident-report | pm-forseti | Community incidents | ✅ New (Phase 2) |
| forseti-company-research | pm-forseti | Research & analysis | ✅ New (Phase 2) |
| forseti-nfr | pm-forseti | NFR documentation | ✅ New (Phase 2) |
| forseti-copilot-agent-tracker | pm-forseti | Agent tracking | ✅ New (Phase 2) |
| forseti-institutional-management | pm-forseti | Institutional governance | ✅ New (Phase 2) |
| forseti-jobhunter-tester | pm-forseti | Job Hunter QA | ✅ New (Phase 2) |
| forseti-agent-evaluation | pm-forseti | Agent evaluation | ✅ New (Phase 2) |

---

## Key Files & Commands

### .gitmodules
- Location: `/home/ubuntu/forseti.life/.gitmodules`
- Content: 20 submodule entries
- Management: Add/remove entries here before `git add`
- Never edit manually during normal operations

### Git Submodule Commands

```bash
# Show all submodules and their commits
git submodule status

# Update all submodules to latest
git submodule foreach 'git checkout main && git pull'

# Initialize submodules (after fresh clone)
git submodule update --init --recursive

# Add a new submodule
git submodule add https://github.com/Forseti-Life/new-repo.git new-repo
git commit -m "Add new-repo as submodule"

# Remove a submodule
git rm new-repo
# Edit .gitmodules to remove [submodule "new-repo"] section
git commit -m "Remove new-repo submodule"
```

### Merge Safety

```bash
# Before merging, back up all 20 submodules
bash workspace-merge-safe.sh --backup

# After successful merge, verify no files deleted
# Exit code 0 = clean merge, no deletions
# Exit code 2 = merge succeeded but sessions/ files deleted (OK)

# If merge fails, auto-restore
bash workspace-merge-safe.sh --restore
```

---

## Independent Push Clones (Special Cases)

Three repos in `/root/` are **NOT** submodules:

- **ai-conversation-push**: Autonomous conversation engine (independent lifecycle)
- **dungeoncrawler-tester-push**: QA utilities (can be updated independently)
- **forseti-cluster-push**: Cluster infrastructure (separate deployment cadence)

These are updated manually via CI/CD push jobs, not coordinated with the main release cycle.

**Exception:** `dungeoncrawler-content-push` is now a **symlink** to the submodule version (single source of truth).

---

## Common Operations

### Scenario 1: A team wants to release a new version

1. Team updates their submodule repo independently
2. Push to `forseti-<product>` repo on GitHub
3. In main repo, `cd forseti-<product> && git pull` to latest
4. Back in main repo: `git add forseti-<product>`
5. Commit: `git commit -m "chore: Update forseti-<product> to latest"`
6. Main repo commit triggers coordinated R1-R4 cycle
7. All 20 repos released simultaneously

### Scenario 2: Cross-repo dependency

Product A depends on new code in Product B:
1. B team commits and pushes to B's repo
2. A team: `cd forseti-b && git pull` (gets new code)
3. Team tests together locally, verifies both work
4. Both teams update main repo pointers (single commit or cascade)
5. Release cycle picks it up

### Scenario 3: Rollback entire platform

```bash
git revert <bad-release-sha>
# All 20 repos automatically rolled back together
```

---

## Governance Rules

1. **No direct commits to submodules from main repo**: Teams commit to their own submodule repo, then main repo updates pointers
2. **Single atomic commit for releases**: One commit pins all 20 submodules
3. **All commits include Co-authored-by trailer**: Maintains authorship across coordinated releases
4. **Merge conflicts resolved at merge time**: Not deferred to submodules
5. **Session state is ephemeral**: Backed up before merge, not tracked permanently in git

---

## Migration from Old Model

This 20-submodule model replaces:
- ❌ 10 separate push clones (inconsistent versions)
- ❌ Missing 10 repos (GitHub-only, hard to track)
- ❌ Duplicate dungeoncrawler-content (now symlinked)

**Phase transition:**
- Phase 1 (✅ Done): Symlink duplicate
- Phase 2 (✅ Done): Clone 10 GitHub-only repos
- Phase 3 (✅ Done): Update .gitmodules, atomic commit
- Phase 4 (🔄 In Progress): Update all instructions, ownership matrix
- Phase 5 (⏳ Pending): Update orchestrator, CI/CD workflows
- Phase 6 (⏳ Pending): Verification & testing
- Phase 7 (⏳ Pending): Team communication & training

---

## See Also

- `runbooks/merge-commit-strategy.md` — Detailed merge/commit governance
- `runbooks/coordinated-release.md` — R1-R4 release cycle procedures
- `runbooks/coordination-policy.md` — Cross-team coordination rules
- `org-chart/DECISION_OWNERSHIP_MATRIX.md` — Who decides what
- `.gitmodules` — Current submodule configuration
