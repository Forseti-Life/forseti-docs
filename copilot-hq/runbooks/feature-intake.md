# Feature Intake Runbook

**Owner:** `ceo-copilot-2` for intake routing, then site PM/BA/PM seats for product disposition  
**Trigger:** Continuous suggestion seeding plus normal seat execution through `feature_request_intake`  
**Scripts:** `scripts/suggestion-intake.sh`, `scripts/route-flow-transitions.py`

---

## Overview

Users interact with Forseti (the AI assistant) via the "Talk to Forseti" channel. When the AI
detects a feature suggestion in the conversation, it automatically creates a `community_suggestion`
Drupal node (status: `new`). These nodes are the raw upstream of the product backlog.

**Pipeline:**

```
User message
    ↓
Talk to Forseti (ai_conversation node)
    ↓  [AI detects [CREATE_SUGGESTION] tag]
community_suggestion node (status: new)
    ↓  [suggestion-intake.sh]
CEO inbox item  →  Flow id: feature_request_intake / Receive Feature Request
    ↓  [CEO / BA / PM execute flow-managed handoffs]
Intake Review → Match Product Team → BA Requirements Review → PM Scope Decision
    ↓  [Approved for delivery]
Prepare Delivery Handoff → launches agentic_sdlc
    ↓  [delivery work may materialize/update feature docs]
Gap analysis / feature documentation / acceptance criteria
    ↓
Acceptance Criteria  →  01-acceptance-criteria.md (criteria tagged [NEW]/[EXTEND]/[TEST-ONLY])
    ↓
QA handoff  →  pm-qa-handoff.sh  →  03-test-plan.md
    ↓  [feature is groomed]
Release scope selection  →  01-change-list.md
    ↓
Normal dev/QA/ship cycle
```

---

## Artifact contract (authoritative)

The intake flow is artifact-driven. Every handoff must produce one canonical artifact that the next seat can consume without guessing.

| Stage | Artifact | Canonical path / system | Produced by | Consumer / next handoff |
|---|---|---|---|---|
| Raw request | Community suggestion record | Drupal `community_suggestion` node | `ai_conversation` / upstream intake surface | `scripts/suggestion-intake.sh` |
| Intake entrypoint | Flow-managed CEO inbox item | `sessions/ceo-copilot-2/inbox/<date>-flow-feature-request-intake-.../command.md` | `scripts/suggestion-intake.sh` | `feature_request_intake` execution |
| Intake routing trail | Flow outboxes / runtime state | `sessions/<seat>/outbox/*.md`, `tmp/flow-runs/feature_request_intake/<run-id>/` | CEO / BA / PM via flow execution | downstream intake node or delivery launch |
| Approved delivery handoff | Delivery entrypoint item | `sessions/<seat>/inbox/<date>-flow-agentic_sdlc-.../command.md` | `route-flow-transitions.py` | delivery flow |
| Accepted backlog item | Feature brief | `features/<feature-id>/feature.md` | PM / BA once delivery/backlog decision is made | BA / PM grooming |
| Problem framing | Problem Statement | `features/<feature-id>/00-problem-statement.md` or equivalent linked intake artifact | PM / BA | Acceptance-criteria authoring |
| Scope contract | Acceptance Criteria | `features/<feature-id>/01-acceptance-criteria.md` | PM | QA test planning + Dev implementation |
| Initial risk contract | Risk Assessment | `features/<feature-id>/06-risk-assessment.md` or linked risk artifact | PM | PM scope decision / release selection |
| QA handoff | QA inbox item | `sessions/qa-<site>/inbox/<item-id>/command.md` | `scripts/pm-qa-handoff.sh` or PM | QA test generation |
| QA planning artifact | Test Plan | `features/<feature-id>/03-test-plan.md` | QA | Stage 0 scope selection / Gate 2 |
| Groomed release input | Change list entry | `sessions/<lead-pm>/artifacts/release-candidates/<release-id>/01-change-list.md` | PM | Dev + QA current-release execution |

Rules:
- `feature.md` is the canonical backlog/work-definition artifact.
- `01-acceptance-criteria.md` is the canonical scope contract for Dev and QA.
- `03-test-plan.md` is QA's planning artifact; the executable PASS/FAIL suite remains the canonical test-case SoT.
- No handoff is considered complete until the downstream artifact exists in its canonical location.

---

## Step 1 — Seed intake continuously

The system continuously seeds new suggestions into the intake flow:

```bash
./scripts/suggestion-intake.sh forseti
```

This will:
- Query Drupal for all `community_suggestion` nodes with `field_suggestion_status = new`
- Write one flow-managed inbox item to `sessions/ceo-copilot-2/inbox/...`
- Mark queried nodes as `under_review` in Drupal
- Print a summary of how many suggestions were found

If there are no new suggestions, it exits cleanly — nothing to do.

---

## Step 2 — Execute the intake flow

The `feature_request_intake` flow now owns review and routing:

1. CEO executes:
   - `Receive Feature Request`
   - `Intake Review`
   - `Match Product Team`
2. BA executes:
   - `BA Requirements Review`
3. PM executes:
   - `PM Scope Decision`
4. If PM approves, the flow launches `agentic_sdlc`
5. If delivery later discovers a scope ambiguity (for example a feature that should be held, deferred, or consolidated into a parent slice), the active `agentic_sdlc` run must branch to `PM Scope Rebaseline` using the exact flow outcome `Scope decision required`

Each flow-managed seat must emit exact `Flow outcome:` lines from `command.md` so the router can advance the next node.

---

## Step 3 — Materialize accepted work

If PM approves the request for delivery, the intake flow launches `agentic_sdlc`.
Feature docs such as `features/<feature-id>/feature.md` may still be created or updated as part of normal PM/BA grooming after intake approval.

For release-stage scoped work, `pm-scope-activate.sh` now seeds the same `agentic_sdlc` runtime directly for the active feature by writing flow-managed `Generate Code` and `Test Cases Review` inbox items plus `tmp/flow-runs/agentic_sdlc/<feature-id>/product-team.json`. That keeps late release activation on the same LangGraph contract as intake-launched work instead of falling back to legacy ad hoc Dev/QA handoffs.

Inside `agentic_sdlc`, scope correction is a first-class flow action:

- Dev or QA may emit `- Flow outcome: Scope decision required` when delivery hits a real scope/ownership ambiguity.
- PM then executes `PM Scope Rebaseline`.
- PM must choose one of the flow outcomes:
  - `Resume implementation`
  - `Resume test design`
  - `Re-scope requirements`
  - `Hold / defer / consolidate`

Do **not** treat hold/defer/consolidate as ad hoc inbox churn outside the flow when the work already lives inside `agentic_sdlc`.

---

## Step 4 — Gap analysis (required before writing AC)

**This step is mandatory.** Do not write AC or hand off to QA until it is complete.

For every requirement in the feature, audit the existing codebase and fill in the `## Gap Analysis` table in `feature.md`. Determine for each requirement whether coverage is **Full**, **Partial**, or **None**, then set the `Feature type:` header field accordingly:

| Finding | Feature type |
|---|---|
| Majority Full coverage | `needs-testing` |
| Majority Partial coverage | `enhancement` |
| Majority None | `new-feature` |

Also record the exact test file path QA should create or extend for each requirement. QA must not guess at locations.

---

## Step 5 — Fill in accepted feature briefs

For each accepted feature, open `features/<feature-id>/feature.md` and complete:

1. **Module assignment** — which Drupal module owns this?
   Check `org-chart/ownership/module-ownership.yaml`
2. **Feature type** — set from gap analysis (`new-feature` / `enhancement` / `needs-testing`)
3. **Acceptance Criteria** — use `templates/01-acceptance-criteria.md`; tag every criterion `[NEW]`, `[EXTEND]`, or `[TEST-ONLY]` per gap analysis
4. **Risk assessment** — use `templates/06-risk-assessment.md`
5. **Priority** — P0 (release blocker), P1 (core value), P2 (nice to have)

---

## Step 5 — Feed into release scope

Once features are triaged and briefs are complete, select which ones enter this release cycle:

1. Add to the release candidate change list: `sessions/pm-forseti/artifacts/release-candidates/<release-id>/01-change-list.md`
2. Scope freeze: no new features added after this point
3. Proceed with the normal release cycle per `runbooks/release-cycle-process-flow.md`

---

## Recurring cadence

| When | Action |
|------|--------|
| **Stage 3 of current release (start)** | Run `suggestion-intake.sh`, triage all `new` items, **run gap analysis**, write AC (tagged), run `pm-qa-handoff.sh` — grooming for NEXT release |
| **Stage 0 of next release** | Pick from groomed pool only — all grooming already done, scope selection is instant |
| **During current release execution** | New suggestions accumulate as `new` in Drupal — do NOT pull until Stage 3 starts |
| **Deferred items** | Remain `deferred` in Drupal; PM resets to `new` manually when ready to re-evaluate |

> **The rule:** grooming for the next release runs during Stage 3 of the current release, in parallel
> with Dev execution. It never holds up the current release. Stage 0 only touches groomed items.

---

## Viewing suggestions in Drupal (manual)

Admins can view all community suggestions at:
- `/admin/content?type=community_suggestion&status=1` (all)
- Filter by `field_suggestion_status` = `new` for unprocessed items

---

## Automation hook (CEO/release monitor)

The release monitor (`scripts/release-kpi-monitor.py`) can be extended to call
`suggestion-intake.sh` automatically when a new release cycle starts (Stage 0 trigger).

To enable, add to the monitor's Stage 0 handler:
```python
subprocess.run(["bash", "scripts/suggestion-intake.sh", site], check=False)
```

---

## Related files

| File | Purpose |
|------|---------|
| `scripts/suggestion-intake.sh` | Pull new suggestions → intake flow entrypoint |
| `scripts/route-flow-transitions.py` | Route intake handoffs and launch delivery |
| `templates/feature-brief.md` | Feature brief template |
| `templates/01-acceptance-criteria.md` | AC template |
| `runbooks/release-cycle-process-flow.md` | Full release cycle (this feeds into Stage 0) |
| `org-chart/sites/forseti.life/site.instructions.md` | Mission statement (use for alignment check) |
