# CEO Coordination Policy (Products + Repository Ownership)

**Last Updated:** 2026-04-23  
**Scope:** Cross-product coordination, repository governance, release management

## Core Principle: Product-Based Separation

Work streams are separated by **product**. Many products are coordinated as submodules in the unified monorepo, while selected product repos can remain standalone when that better matches ownership and deployment needs. Releases are still coordinated through the main repository's R1-R4 gates where applicable.

## Repository Structure

The monorepo contains coordinated submodules plus independent product repos:

**Standalone product repos on this host:**
- dungeoncrawler-pf2e

**Coordinated submodules:**
- dungeoncrawler-content, forseti-shared-modules, forseti-devops, forseti-meshd, forseti-mobile, forseti-docs, forseti-platform-specs, forseti-job-hunter, h3-geolocation

**New (10):**
- forseti-safety-content, forseti-safety-calculator, forseti-content, forseti-community-incident-report, forseti-company-research, forseti-nfr, forseti-copilot-agent-tracker, forseti-institutional-management, forseti-jobhunter-tester, forseti-agent-evaluation

**Independent (3 push clones in /root/):**
- ai-conversation-push, dungeoncrawler-tester-push, forseti-cluster-push

## Product Manager (PM) Ownership

PMs own work at the **submodule directory level**. Each PM is responsible for their product's submodule(s) in the monorepo.

| Product | Team PM | Submodule(s) | Decision Authority |
|---------|---------|--------------|-------------------|
| DungeonCrawler | pm-dungeoncrawler | dungeoncrawler-pf2e, dungeoncrawler-content | Feature scope, ship/no-ship |
| Forseti (main) | pm-forseti | forseti-shared-modules, forseti-mobile, forseti-docs, forseti-platform-specs, forseti-job-hunter | Feature scope, ship/no-ship |
| Forseti Safety | pm-forseti | forseti-safety-content, forseti-safety-calculator | Feature scope, ship/no-ship |
| Forseti Community | pm-forseti | forseti-community-incident-report, forseti-content | Feature scope, ship/no-ship |
| Forseti Research | pm-forseti | forseti-company-research, forseti-nfr | Feature scope, ship/no-ship |
| Forseti Agent Tracker | pm-forseti | forseti-copilot-agent-tracker, forseti-agent-evaluation | Feature scope, ship/no-ship |
| Infrastructure | pm-infra | forseti-devops | Deployment, DevOps, scaling decisions |

## Decision Ownership Baseline

- Organization-wide decision and RACI baseline: `org-chart/DECISION_OWNERSHIP_MATRIX.md`
- Submodule-level decisions: See table above (PM owns their submodules)
- Release coordination: CEO (Copilot) coordinates R1-R4 cycle
- Cross-submodule conflicts: Escalated via coordination-policy (see below)

## Submodule-Level Boundaries (Required)

- **Code ownership** is enforced at the **submodule directory** level in Git
- Each submodule has its own branch protection rules and code review process
- Non-CEO agents must stay within file scopes defined in `org-chart/agents/instructions/<agent-id>.instructions.md`
- If work requires changes outside your owned scope, open a **passthrough request** to the owning PM

## Ownership Definition

A PM is the decision-maker for their submodules' scope:
- Roadmap and feature scope
- Acceptance criteria and test cases
- Ship/no-ship recommendation (with QA + CEO input)
- Priority within their submodule(s)
- API contracts (if providing shared utilities)

## Coordinated Release Model (R1-R4)

All 20 submodules are version-locked in single atomic commits:

1. **R1 (Ready):** All teams confirm submodules ready for release
2. **R2 (Review):** Full integration test of all 20 submodules together
3. **R3 (Release Commit):** Single commit pins all 20 submodules to release versions
4. **R4 (Rollout):** Deploy all 20 repos simultaneously

See `runbooks/coordinated-release.md` for detailed procedures.

## Cross-Submodule Dependencies

If Product A depends on new code in Product B:

1. **B team** commits and pushes to their submodule repo
2. **A team** pulls B's submodule to get new code: `cd forseti-b && git pull`
3. **Both teams** test together locally, verify compatibility
4. **Main repo** updates both submodule pointers in coordinated commit
5. **Release cycle** picks up both changes

### Passthrough Process (Optional Formality)

For less urgent cross-submodule work:
1. Requesting PM opens passthrough request (problem statement + acceptance criteria)
2. CEO (Copilot) coordinates sequencing, ensures consistency
3. Owning PM may:
   - Accept and schedule
   - Propose alternative interface/contract
   - Reject with rationale and suggested path

## Conflicts & Escalation

When teams receive conflicting requests or cross-submodule changes create friction:

1. **CEO attempts to reconcile** via:
   - Scope split (change subset into independent tasks)
   - Prioritization (sequence changes over time)
   - Interface contract (agree on data/API boundary)

2. **If unresolved or high-risk:**
   - CEO escalates to Board (human owner) with options and tradeoffs

3. **If time-critical & acceptable risk:**
   - CEO may make a call, document in session updates, communicate to all affected teams

## Merge Safety & Release Gates

Before ANY merge into main repo:

1. `workspace-merge-safe.sh` backs up all 20 submodules
2. Merge proceeds with full conflict resolution
3. If merge succeeds but deletions occurred (exit code 2):
   - Sessions/ files were auto-deleted (expected behavior)
   - Release ready to proceed
4. If merge fails, all 20 repos automatically restored

See `runbooks/merge-commit-strategy.md` for full procedures.

## Special Rules: Push Clones

Three independent push clones in `/root/` follow different rules:
- **NOT** version-locked with main repo
- Updated via independent CI/CD jobs
- Can have different release cadence
- Useful for infrastructure, utilities, independent tools

Exception: `dungeoncrawler-content-push` is now a **symlink** to the submodule (unified single source of truth).

## Submodule Maintenance

Adding a new submodule:
```bash
git submodule add https://github.com/Forseti-Life/new-repo.git new-repo
git commit -m "Add new-repo as submodule"
# Assign PM ownership in this policy file
```

Removing a submodule:
```bash
git rm new-repo
# Edit .gitmodules to remove [submodule "new-repo"] section
git commit -m "Remove new-repo submodule"
```

## See Also

- `runbooks/monorepo-structure.md` — Architecture of 20-submodule model
- `runbooks/merge-commit-strategy.md` — Detailed merge/commit governance
- `runbooks/coordinated-release.md` — R1-R4 release procedures
- `org-chart/DECISION_OWNERSHIP_MATRIX.md` — Who decides what organization-wide
