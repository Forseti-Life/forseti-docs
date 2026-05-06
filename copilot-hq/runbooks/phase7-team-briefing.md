# Phase 7 Team Communication — 20-Submodule Architecture Launch

**Date:** 2026-04-23  
**Status:** ✅ PRODUCTION READY  
**Target Audience:** All Development Teams (PM, Dev, QA, BA, Sec)

---

## EXECUTIVE SUMMARY: UNIFIED 20-SUBMODULE MONOREPO

All 25 Forseti-Life GitHub repositories are now integrated into a **unified monorepo structure** with coordinated release cycles. This document explains the new architecture, your role in it, and how to work effectively with the 20-submodule model.

### What Changed

**Before (Scattered):**
- 25 independent repositories across GitHub
- No coordinated release mechanism
- Manual synchronization between related repos
- Unclear ownership and coordination

**After (Unified):**
- 1 main monorepo (copilot-hq) containing 20 nested submodules
- All submodules coordinated in single atomic commits
- Clear team ownership matrix
- Automated release cycles with safety gates

### Key Facts

| Fact | Value |
|------|-------|
| Main Repository | copilot-hq (Forseti-Life/copilot-hq) |
| Submodules (Tier 2) | 20 repos (10 existing + 10 new) |
| Push Clones (Tier 3) | 3 independent utilities + 1 symlink |
| Coordinated Releases | Yes (all 20 submodules in atomic commit) |
| Team Coordination | Via coordination-policy.md passthrough requests |
| Merge Safety | workspace-merge-safe.sh verifies all 20 repos |

---

## NEW ARCHITECTURE: 3-TIER SYSTEM

### Tier 1: Main Monorepo (copilot-hq)
```
Location: /home/ubuntu/forseti.life/
Remote: https://github.com/Forseti-Life/copilot-hq.git
Purpose: Control plane for orchestration, release cycle, CI/CD
```

### Tier 2: 20 Git Submodules
**Tier 2A: Existing 10 Repos**
1. dungeoncrawler-content
2. dungeoncrawler-pf2e
3. forseti-devops
4. forseti-docs
5. forseti-job-hunter
6. forseti-meshd
7. forseti-mobile
8. forseti-platform-specs
9. forseti-shared-modules
10. h3-geolocation

**Tier 2B: NEW 10 Repos (Now Integrated)**
11. forseti-safety-content
12. forseti-safety-calculator
13. forseti-content
14. forseti-community-incident-report
15. forseti-company-research
16. forseti-nfr
17. forseti-copilot-agent-tracker
18. forseti-institutional-management
19. forseti-jobhunter-tester
20. forseti-agent-evaluation

### Tier 3: 3 Independent Push Clones
- `/root/ai-conversation-push/` (forseti-ai-conversation)
- `/root/dungeoncrawler-tester-push/` (dungeoncrawler-tester)
- `/root/forseti-cluster-push/` (forseti-cluster)
- `/root/dungeoncrawler-content-push/` → symlink to Tier 2B

---

## TEAM OWNERSHIP MATRIX

See `runbooks/repo-ownership-matrix.md` for complete ownership details.

Each of the 20 submodules is owned by a team (PM, Dev, QA, BA, Sec):

**Example:**
- **forseti-job-hunter**: PM=pm-forseti, Dev=dev-forseti, QA=qa-forseti
- **dungeoncrawler-pf2e**: PM=pm-dungeoncrawler, Dev=dev-dungeoncrawler, QA=qa-dungeoncrawler
- **forseti-safety-content**: PM=pm-open-source, Dev=dev-open-source

Your team owns specific submodules. All other repos are "passthrough" scope.

---

## COORDINATED RELEASE MODEL

### What "Coordinated Release" Means

All 20 submodules are released **together in a single atomic commit**:

1. **R1 (Development):** Teams make changes to their submodules
2. **R2 (Testing):** QA tests all 20 repos together
3. **R3 (Sign-Off):** PM signs off on all 20 repos (single approval)
4. **R4 (Production Push):** Single git commit with all 20 submodule pointers

**Benefit:** No orphaned submodules; all changes deployed atomically.

### Release Cycle Flow

```
┌─────────────────────────────────────────────────────────────┐
│ orchestrator-loop.sh (every 60 seconds)                      │
│                                                               │
│ 1. consume_replies     → inboxes loaded                      │
│ 2. dispatch_commands   → routes requests to teams            │
│ 3. release_cycle       → checks R1-R4 progress              │
│ 4. pick_agents         → highest ROI agents                  │
│ 5. exec_agents         → agents execute work                 │
│ 6. health_check        → monitors stalled agents             │
│ 7. kpi_monitor         → detects stagnation                  │
│ 8. publish             → dashboard updates                   │
└─────────────────────────────────────────────────────────────┘

ALL 20 SUBMODULES TRACKED IN SINGLE RELEASE CYCLE
```

### What Teams Must Do

- **PM:** Groom features, sign off on releases (all 20 repos at once)
- **Dev:** Implement features in owned submodules
- **QA:** Test all 20 submodules together before sign-off
- **Cross-Submodule Work:** Use passthrough request process (see below)

---

## DEVELOPER WORKFLOW

### Setup: Clone with All Submodules

```bash
# Clone the monorepo WITH all 20 submodules
git clone --recurse-submodules https://github.com/Forseti-Life/copilot-hq.git

# Or, if you already have it cloned:
cd /home/ubuntu/forseti.life
git submodule update --init --recursive
```

### Working Within Your Owned Submodule

```bash
cd /home/ubuntu/forseti.life/forseti-job-hunter

# Make changes to YOUR submodule (normal git workflow)
git checkout -b feature/new-feature
echo "changes" > file.txt
git add file.txt
git commit -m "Feature: add new feature"
git push origin feature/new-feature
```

### Creating a PR in Your Submodule

Your submodule is a **full independent Git repository**:
- Create PRs on GitHub normally (e.g., keithaumiller/forseti-job-hunter)
- Merge PRs as usual
- Your changes appear in the parent monorepo automatically

### Getting Latest Submodule Changes

```bash
cd /home/ubuntu/forseti.life

# Update all 20 submodules to latest
git submodule update --recursive

# Or pull with submodule updates
git pull --recurse-submodules
```

---

## CROSS-SUBMODULE COORDINATION

### When Your Work Needs Changes in Another Submodule

**Use the Passthrough Request Process:**

1. **Identify the owning team** (see repo-ownership-matrix.md)
2. **Create a passthrough request inbox item** (example):
   ```
   sessions/ceo-copilot-2/inbox/
   └── 20260423-needs-dev-dungeoncrawler-add-halfling-ancestry/
       ├── command.md
       └── roi.txt
   ```
3. **Describe the request** in command.md with:
   - What change you need
   - Why you need it
   - How it affects your release timeline

4. **Orchestrator routes it** → dev-dungeoncrawler inbox
5. **Team executes** → changes go into the standalone `dungeoncrawler-pf2e` product repo
6. **You benefit** when your coordinated release includes their changes

See `runbooks/coordination-policy.md` for details.

---

## MERGE SAFETY & COORDINATED PUSH

### Pre-Merge Safety Gate (workspace-merge-safe.sh)

Before any merge involving the monorepo:

```bash
# Verify all 20 submodules are clean (no uncommitted changes)
bash scripts/workspace-merge-safe.sh --dry-run

# If dry-run passes:
# Then execute the real merge
bash scripts/workspace-merge-safe.sh <branch-or-commit>
```

**What it does:**
1. Verifies all 20 submodules have 0 uncommitted changes
2. Backs up sessions/ and .gitmodules
3. Executes git merge
4. Post-merge: verifies all 20 submodule pointers intact

**Exit codes:**
- 0 = merge OK, all checks passed
- 1 = merge aborted (safety issue)
- 2 = merge OK but warnings (manual review needed)

### Coordinated Push (all 20 at once)

When pm-forseti is ready to push a release:

```bash
# All 20 submodules pushed in single atomic commit
git push origin main

# GitHub Actions workflow:
# 1. Detects push
# 2. Clones with --recurse-submodules
# 3. Verifies all 20 submodules initialized
# 4. Deploys all 20 repos in sequence
```

---

## DEPLOYMENT IMPACT

### GitHub Actions Deploy Workflow

**Change:** Added `--recurse-submodules` to clone command

```bash
git clone --recurse-submodules --branch master "$REPO_URL"
```

**Effect:**
- GitHub Actions now initializes all 20 submodules during deployment
- All 20 repos available for deployment scripts
- Same atomic deployment as monorepo

---

## DOCUMENTATION & REFERENCES

Read these in order:

1. **runbooks/monorepo-structure.md** (NEW)
   - Complete architecture explanation
   - 20-submodule coordinated model rationale
   - Developer and operator workflows

2. **runbooks/repo-ownership-matrix.md** (NEW)
   - All 20 submodules with team ownership
   - Escalation contacts
   - Responsibility assignments

3. **runbooks/coordination-policy.md** (UPDATED)
   - Passthrough request process
   - Cross-submodule dependency procedures
   - Team separation rules

4. **runbooks/merge-commit-strategy.md** (UPDATED)
   - Pre-merge safety gate procedures
   - Merge conflict resolution for .gitmodules
   - 20-submodule backup and restore

5. **runbooks/coordinated-release.md** (Reference)
   - Release cycle stages (R1-R4)
   - Coordination requirements

---

## FREQUENTLY ASKED QUESTIONS

### Q: Do I need to clone all 20 submodules?

**A:** For development, yes — use `git clone --recurse-submodules`. 
For viewing or CI/CD, you can shallow clone if needed. GitHub Actions handles this automatically.

### Q: Can I still create PRs in my submodule?

**A:** Yes! Each submodule is a full Git repository. Create PRs normally on GitHub.
Changes merged to main in your submodule automatically appear in the monorepo.

### Q: What if I only care about one submodule?

**A:** You can:
1. Clone the monorepo and cd to your submodule
2. Or clone just that submodule independently
3. Either way, you work with normal Git workflows

### Q: How do I request changes in another team's submodule?

**A:** Use the passthrough request process in sessions/ceo-copilot-2/inbox/.
See `runbooks/coordination-policy.md` § Passthrough Requests.

### Q: What if a merge breaks one of the 20 submodules?

**A:** The merge safety gate (workspace-merge-safe.sh) detects this.
Exit code 1 = merge aborted (safety prevented the break).
Exit code 2 = merge allowed but manual review needed.

### Q: How is the release cycle different now?

**A:** Instead of 20 independent releases, there's ONE coordinated release:
- Single R1 → R2 → R3 → R4 cycle for all 20 repos
- Single PM sign-off
- Single atomic push

### Q: Can individual submodules still have their own releases?

**A:** Not via the coordinated cycle. But teams can:
1. Tag releases in their submodule repo (GitHub Tags)
2. Maintain independent release notes (submodule README)
3. Reference those in your team documentation

---

## GETTING HELP

**Questions about:**
- **Architecture / Setup** → See runbooks/monorepo-structure.md
- **Team Ownership** → See runbooks/repo-ownership-matrix.md
- **Coordinating Work** → See runbooks/coordination-policy.md
- **Merge Safety** → See runbooks/merge-commit-strategy.md
- **Release Cycle** → See runbooks/coordinated-release.md

**Escalate to:**
- CEO (ceo-copilot-2): Major architecture decisions
- Your PM: Day-to-day coordination
- dev-infra: Deployment and CI/CD issues

---

## TIMELINE & NEXT STEPS

**✅ Completed (as of 2026-04-23):**
- All 20 submodules on filesystem
- .gitmodules metadata created and verified
- workspace-merge-safe.sh enhanced for 20 submodules
- GitHub Actions workflow updated
- Documentation complete and published
- Verification tests: ALL PASS

**Next Steps:**
1. Read this briefing and linked runbooks
2. Clone monorepo with `--recurse-submodules`
3. Verify you can cd to your owned submodules
4. Familiar yourself with passthrough request process
5. Ask questions in team meetings

---

## SIGN-OFF

| Role | Status | Date |
|------|--------|------|
| CEO (ceo-copilot-2) | ✅ Approved | 2026-04-23 |
| Architecture Review | ✅ Passed | 2026-04-23 |
| Verification Testing | ✅ All Pass | 2026-04-23 |
| Team Briefing | 📋 Ready | 2026-04-23 |

---

## QUESTIONS?

Post questions in the team Slack channel or escalate to your PM.

Welcome to the unified 20-submodule monorepo! 🚀
