# Repository Ownership Matrix

**Generated:** 2026-04-23  
**Effective:** Immediately (after Phase 4 completion)  
**Maintained by:** CEO/Orchestration  
**Review Cycle:** Quarterly or on team changes

---

## 20 Submodule Owners (Coordinated Release Model)

All 20 submodules are version-locked together in R1-R4 coordinated releases.

| # | Submodule | GitHub Repo | Primary Owner (PM) | Dev Lead | QA Lead | Purpose | Status |
|---|-----------|-------------|-------------------|----------|---------|---------|--------|
| 1 | dungeoncrawler-pf2e | Forseti-Life/dungeoncrawler-pf2e | pm-dungeoncrawler | dev-dungeoncrawler | qa-dungeoncrawler | PF2E content & game engine | ✅ Active |
| 2 | dungeoncrawler-content | Forseti-Life/dungeoncrawler-content | pm-dungeoncrawler | dev-dungeoncrawler | qa-dungeoncrawler | Shared DungeonCrawler content | ✅ Active |
| 3 | forseti-shared-modules | Forseti-Life/forseti-shared-modules | pm-forseti | dev-forseti | qa-forseti | Shared utilities & common functions | ✅ Active |
| 4 | forseti-devops | Forseti-Life/forseti-devops | pm-infra | dev-infra | qa-infra | Infrastructure, deployment scripts | ✅ Active |
| 5 | forseti-meshd | Forseti-Life/forseti-meshd | pm-forseti | dev-forseti | qa-forseti | Mesh networking service | ✅ Active |
| 6 | forseti-mobile | Forseti-Life/forseti-mobile | pm-forseti | dev-forseti | qa-forseti | Mobile application (iOS/Android) | ✅ Active |
| 7 | forseti-docs | Forseti-Life/forseti-docs | pm-forseti | dev-forseti | qa-forseti | Public documentation website | ✅ Active |
| 8 | forseti-platform-specs | Forseti-Life/forseti-platform-specs | pm-forseti | dev-forseti | qa-forseti | API specs, standards, design docs | ✅ Active |
| 9 | forseti-job-hunter | Forseti-Life/forseti-job-hunter | pm-forseti | dev-forseti | qa-forseti | Job Hunter SaaS product | ✅ Active |
| 10 | h3-geolocation | Forseti-Life/h3-geolocation | pm-forseti | dev-forseti | qa-forseti | H3 geolocation utility library | ✅ Active |
| 11 | forseti-safety-content | Forseti-Life/forseti-safety-content | pm-forseti | dev-forseti | qa-forseti | Safety content library (NEW) | ✅ New (Phase 2) |
| 12 | forseti-safety-calculator | Forseti-Life/forseti-safety-calculator | pm-forseti | dev-forseti | qa-forseti | Safety calculation engine (NEW) | ✅ New (Phase 2) |
| 13 | forseti-content | Forseti-Life/forseti-content | pm-forseti | dev-forseti | qa-forseti | General content repository (NEW) | ✅ New (Phase 2) |
| 14 | forseti-community-incident-report | Forseti-Life/forseti-community-incident-report | pm-forseti | dev-forseti | qa-forseti | Community incident tracking (NEW) | ✅ New (Phase 2) |
| 15 | forseti-company-research | Forseti-Life/forseti-company-research | pm-forseti | dev-forseti | qa-forseti | Research & analysis repository (NEW) | ✅ New (Phase 2) |
| 16 | forseti-nfr | Forseti-Life/forseti-nfr | pm-forseti | dev-forseti | qa-forseti | Non-functional requirements docs (NEW) | ✅ New (Phase 2) |
| 17 | forseti-copilot-agent-tracker | Forseti-Life/forseti-copilot-agent-tracker | pm-forseti | dev-forseti | qa-forseti | Agent lifecycle tracking (NEW) | ✅ New (Phase 2) |
| 18 | forseti-institutional-management | Forseti-Life/forseti-institutional-management | pm-forseti | dev-forseti | qa-forseti | Institutional governance (NEW) | ✅ New (Phase 2) |
| 19 | forseti-jobhunter-tester | Forseti-Life/forseti-jobhunter-tester | pm-forseti | dev-forseti | qa-forseti | Job Hunter QA & testing (NEW) | ✅ New (Phase 2) |
| 20 | forseti-agent-evaluation | Forseti-Life/forseti-agent-evaluation | pm-forseti | dev-forseti | qa-forseti | Agent evaluation framework (NEW) | ✅ New (Phase 2) |

---

## Independent Push Clones (NOT Coordinated)

These repos in `/root/` follow independent release cadences:

| # | Directory | GitHub Repo | Primary Owner | Purpose | Status |
|---|-----------|-------------|------------------|---------|--------|
| 21 | ai-conversation-push | Forseti-Life/forseti-ai-conversation | pm-forseti | Autonomous AI conversation engine | ✅ Active |
| 22 | dungeoncrawler-tester-push | Forseti-Life/dungeoncrawler-tester | pm-dungeoncrawler | DungeonCrawler QA utilities | ✅ Active |
| 23 | forseti-cluster-push | Forseti-Life/forseti-cluster | pm-infra | Cluster infrastructure utilities | ✅ Active |
| 24 | dungeoncrawler-content-push | → SYMLINK to submodule #2 | --- | **Single source of truth in monorepo** | ✅ Symlinked |

---

## Escalation Path

### For Code/Feature Decisions Within a Submodule
1. **PM for that submodule** (decision maker on scope, acceptance criteria, ship/no-ship)
2. **Dev Lead** implements; **QA Lead** validates
3. If blocked: escalate to **CEO** (Copilot) for coordination

### For Cross-Submodule Dependencies
1. **Requesting PM** opens **passthrough request** to owning PM
2. **CEO** coordinates sequencing and timeline
3. Both PMs agree on interface/contract
4. Changes land in single coordinated commit (R3 release gate)

### For Release Cycle Issues
1. **Release Coordinator** (pm-forseti by default) manages R1-R4 gates
2. If blocked: escalate to **CEO** for decision
3. If high-risk or time-critical: escalate to **Board** (human owner)

### For Merge Conflicts / Repo Health
1. **CEO** analyzes conflict
2. Resolves by **scope ownership** (which PM owns affected code?)
3. Contacts owning PM for decision
4. Documents resolution in commit message

---

## Ownership Rules

### Submodule Decisions

A **PM owns** their submodule(s) and decides:
- ✅ Feature scope and acceptance criteria
- ✅ Roadmap prioritization (within their submodule)
- ✅ Ship/no-ship recommendation (with QA input)
- ✅ API contracts (if providing shared utilities)
- ✅ Code review standards for their team
- ✅ Testing strategy and QA gates

A PM **does NOT own**:
- ❌ Other PMs' submodules (must use passthrough process)
- ❌ Submodule scheduling (CPU/deployment resource) — that's pm-infra
- ❌ Release cycle timing (that's CEO/Release Coordinator)
- ❌ Organization-wide architecture decisions (that's Board)

### Dev Lead Responsibilities

Each dev-* lead is responsible for:
- ✅ Code quality within their team's submodules
- ✅ Merge request reviews for their team
- ✅ Technical design decisions for their team
- ✅ Coordination with other teams (via PM)
- ✅ Escalation to their PM if blocked

### QA Lead Responsibilities

Each qa-* lead is responsible for:
- ✅ Test coverage for their team's submodules
- ✅ QA sign-off before each release
- ✅ Regression testing after merges
- ✅ Escalation to their PM if quality issues detected

### Release Coordinator Responsibilities

**pm-forseti** (default Release Coordinator) is responsible for:
- ✅ R1 (Ready): Verify all 20 submodules ready
- ✅ R2 (Review): Run full integration tests
- ✅ R3 (Release Commit): Create single atomic commit pinning all 20 submodules
- ✅ R4 (Rollout): Deploy all 20 repos simultaneously
- ✅ Escalation to CEO if any gate cannot be satisfied

---

## Adding a New Submodule

**Process:**
1. PM (or CEO) identifies new repo to add
2. Clone into `/home/ubuntu/forseti.life/`
3. Add entry to `.gitmodules`
4. `git add` and commit: `"Add <repo-name> as submodule"`
5. Update this **repo-ownership-matrix.md** with ownership details
6. Update `runbooks/coordination-policy.md` to reflect new PM ownership
7. Assign team in next **R1-R4 coordinated release cycle**

**Who can add?** CEO (Copilot) or authorized PM (must have been approved by Board in planning phase).

---

## Removing a Submodule

**Process:**
1. PM (or CEO) identifies repo to remove
2. Verify no active development depends on it
3. `git rm <repo-name>` from main repo
4. Edit `.gitmodules` to remove `[submodule "<repo-name>"]` section
5. Commit: `"Remove <repo-name> submodule — no longer needed"`
6. Update this matrix to reflect change
7. Archive the GitHub repo (do not delete; maintain audit trail)

**Who can remove?** Only CEO or Board authorization required.

---

## Cross-Team Dependencies

If multiple teams' work must coordinate:

1. **pm-forseti** is the default **Release Coordinator** and arbitrates scheduling
2. **CEO** helps schedule coordinated commits
3. **All changes** land in single atomic commit (R3 release gate)
4. **No cascading merges** — one commit or nothing

**Example:** forseti-job-hunter adds new API that forseti-mobile consumes:
- Job Hunter team commits new API to forseti-job-hunter
- Mobile team updates forseti-mobile to consume new API (tests locally)
- Both teams push their commits
- **R3 release commit** pins both submodules to compatible versions
- **R4** deploys both together — no version skew

---

## Team Contacts

| Role | Person/Team | Slack | Email |
|------|-------------|-------|-------|
| **Board** | Keith Miller (CEO) | @keithaumiller | keith@forseti.life |
| **CEO/Orchestration** | Copilot (ceo-copilot-2) | #ceo-coordination | — |
| **Release Coordinator** | pm-forseti | #pm-forseti | — |
| **Infrastructure PM** | pm-infra | #pm-infra | — |
| **DungeonCrawler PM** | pm-dungeoncrawler | #pm-dungeoncrawler | — |

---

## See Also

- `runbooks/monorepo-structure.md` — Architecture of 20-submodule model
- `runbooks/coordination-policy.md` — Cross-team coordination rules
- `runbooks/coordinated-release.md` — R1-R4 release cycle procedures
- `org-chart/DECISION_OWNERSHIP_MATRIX.md` — Organization-wide decision matrix
- `.gitmodules` — Current submodule configuration
