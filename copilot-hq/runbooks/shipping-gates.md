# Shipping Gates (Checks & Balances)

Master process flow (authoritative): `runbooks/release-cycle-process-flow.md`

## Gate artifact map (authoritative)

| Gate / boundary | Canonical artifacts | Producer | Consumer / next handoff |
|---|---|---|---|
| Gate 0 — Intake | `00-problem-statement.md`, `01-acceptance-criteria.md`, `06-risk-assessment.md`, intake `command.md` | PM / BA / requester lane | PM triage + grooming |
| Gate 1 — Implementation ready | `02-implementation-notes.md` (or equivalent dev notes) | Dev | QA planning + PM release assembly |
| Gate 1b — Code review dispatch | `agent-code-review` outbox, dev inbox finding items, PM risk-acceptance artifact | Code review seat + PM | Dev remediation or PM risk decision |
| Gate 1c — Hotfix review | Hotfix code-review inbox/outbox pair | CEO / PM + code-review seat | PM follow-up routing |
| Gate 2 — Verification | `03-test-plan.md`, QA verification report, audit artifacts, release `02-test-evidence.md` updates | QA | PM signoff flow |
| Release readiness boundary | PM signoff artifacts + operator push-ready inbox item | `scripts/release-signoff.sh` | Release operator (`pm-forseti` by default) |
| Gate 4 — Post-release verification | Production audit artifacts + post-release verification note | QA | Next release scoping / remediation decisions |

Rules:
- A gate is not complete until its canonical artifact exists in the path above.
- The release operator consumes the push-ready inbox item; the push itself is a handoff boundary, not a substitute for the required artifacts.
- Release state advancement happens only after `post-coordinated-push.sh`, never on signoff alone.
- **Signoff source-of-truth rule:** PM signoff is complete only when `sessions/<pm-seat>/artifacts/release-signoffs/<release-id>.md` exists. Narrative outboxes claiming the script was run do **not** count as signoff completion.

## Gate 0 — Intake (Any role)
Required artifacts:
- Problem Statement
- Acceptance Criteria
- Risk Assessment (initial)

Release-cycle rule:
- Intake is always allowed, but once a release cycle starts and scope is frozen, new intake is for the **next** release cycle (or deferred) unless PM explicitly re-baselines the cycle.

Exit criteria:
- Scope and non-goals are explicit.
- Permissions and failure modes are defined.

## Gate 1 — Implementation Ready (Dev)
Required artifacts:
- Implementation Notes (draft)

Exit criteria:
- Approach matches acceptance criteria.
- Identified tests to run.
- **Cross-site module sync check (required):** If this change touches a module present in both forseti and dungeoncrawler (`web/modules/custom/`), confirm the equivalent fix is applied to the other site in the same commit or an immediate follow-on inbox item. Implementation notes must state: "Cross-site sync: applied / not applicable (reason)." (Added 2026-04-05 — GAP-DC-MODULE-DIVERGENCE: Bedrock model fix applied to forseti was not propagated to dungeoncrawler until `error-fixes-batch-1`, causing a live EOL-model error.)

## Gate 1b — Code Review Finding Dispatch (PM, required before Gate 2)

Current automation note:
- The release-cycle pre-ship code-review item is now emitted as a flow-managed `release_shipping_flow` **Release Code Review** step.
- PM follow-up for unresolved MEDIUM+ findings is now emitted as a flow-managed `release_shipping_flow` **PM Code Review Triage** step.
- The operator push-ready item is now emitted as a flow-managed `release_shipping_flow` **Coordinated Push** step.
- The LangGraph registry/UI now includes `release_shipping_flow` as the first-class release representation.
- Alignment rule: `release_shipping_flow` is the release-only validation/signoff wrapper. If Gate 1b or Gate 2 discovers delivery work, that work returns to `agentic_sdlc`; release does not own a separate long-lived remediation loop.
- Gate 2, PM signoff, coordinated push, and release advancement are still enforced by scripts and repo-state guards; those back-half steps have not yet been fully migrated to flow-managed execution.

**Release Code Review handoff contract (required):**
- The `agent-code-review` `command.md` must identify the release id, release start time, and the scoped feature artifact paths for the active release.
- Reviewer verdicts must cite the exact reviewed artifact paths in the outbox summary or findings.
- Missing or incomplete release handoff evidence is **not** a silent blocker: record it as a routed finding (MEDIUM+) so PM triage can repair the handoff or route the underlying work.

After each `agent-code-review` run for a release cycle, PM must:
1. Read the code-review outbox for that release: `sessions/agent-code-review/outbox/<date>-code-review-<site>-<release-id>.md`
2. For every finding rated **MEDIUM or higher**, create a dev-seat inbox item **within the same release cycle**:
   - Folder: `sessions/<dev-seat>/inbox/<date>-cr-finding-<finding-id>/`
   - Required fields in `command.md`: finding ID, file path, severity, description, fix approach (if known), acceptance criteria
   - Required: `roi.txt` (use severity as proxy: CRITICAL→10, HIGH→8, MEDIUM→6)
3. If risk acceptance is chosen instead of a fix, record the decision explicitly in `sessions/pm-<site>/artifacts/risk-acceptances/` with rationale and sign-off owner.

**Exit criteria (Gate 1b):**
- All MEDIUM+ findings either have a dev-seat inbox item OR an explicit risk-acceptance record.
- No MEDIUM+ finding may be left unrouted (i.e., visible only in the code-review outbox).

**Gate sequencing:** Gate 1b must complete before PM may record a release signoff (`scripts/release-signoff.sh`).
- **Reminder/readiness rule:** CEO/PM seats must not dispatch or honor a signoff-ready/reminder state until this Gate 1b exit criteria is satisfied in repo state.

**Lesson (2026-03-19):** In dungeoncrawler release-a, finding F-DC-A-1 (MEDIUM: CAST LIKE on LONGTEXT columns, `copilot_agent_tracker`) went untracked from Mar 9 to Mar 19 — triggering an unplanned extra QA cycle at Gate 2 (8 violations, commit `175b7c3b4`).

## Gate 1c — Hotfix Code Review (required for CEO/PM-applied changes)

When any CEO or PM seat applies code changes directly (bypassing a dev inbox item flow — e.g., during a production outage response), a code review inbox item MUST be created for `agent-code-review` within the same session:
- Folder: `sessions/agent-code-review/inbox/<date>-hotfix-cr-<site>-<description>/`
- Required fields in `command.md`: file paths changed, change summary, and reason for bypassing dev inbox flow
- Required: `roi.txt` (use severity: CRITICAL outage → 10, HIGH risk → 8)

**Exit criteria (Gate 1c):**
- `agent-code-review` outbox exists for the hotfix with explicit PASS/FAIL per file.
- Any MEDIUM+ finding triggers a dev inbox item for the owning PM seat.
- This gate does not block deployment in progress (hotfix may ship); it must complete within the same release cycle.

**Gate sequencing:** Gate 1c runs concurrently with or after hotfix deployment; it does not block Gate 1b for normal release scope. Gate 1c findings feed into Gate 1b dispatch for the current or next release cycle.

**KB reference:** `knowledgebase/lessons/20260405-hotfix-code-review-gate-gap.md`

## Gate 2 — Verification (Tester)
Required artifacts:
- Test Plan
- Verification Report
- Methodology reference (required): `runbooks/role-based-url-audit.md` (URL/access validation by role; localhost-first)

Gate 2 integration contract:
- **Inputs:** active release ID, scoped feature list, feature-level QA evidence, suite/audit outputs, and current acceptance criteria
- **Outputs:** one release-scoped QA decision artifact containing the exact release ID and explicit APPROVE/BLOCK, plus supporting test evidence
- **Consumers:** PM signoff flow, `scripts/release-signoff.sh`, `scripts/release-signoff-status.sh`, and `scripts/ceo-release-health.sh`

Canonical Gate 2 artifact filenames:
- `sessions/qa-<team>/outbox/<timestamp>-gate2-approve-<release-id>.md`
- `sessions/qa-<team>/outbox/<timestamp>-gate2-block-<release-id>.md`
- Exception approvals recognized by automation:
  - `...-gate2-waiver-<release-id>.md`
  - legacy `...-empty-release-self-cert-<release-id>.md`

Rules:
- The artifact body must contain the exact release ID and the exact verdict word.
- Feature-level verification reports and targeted retest notes do **not** complete Gate 2 unless one of the canonical release-scoped artifacts above exists.
- **Latest canonical Gate 2 artifact wins.** If a newer `gate2-block` exists after an older `gate2-approve`, the release is blocked until QA writes a newer approval/waiver/self-cert artifact.

Test-case source of truth requirement:
- Test cases must reside in a central executable automation suite with PASS/FAIL outcomes.
- The release candidate must record which automated suites were run and the results (see `templates/release/02-test-evidence.md`).

Exit criteria:
- Evidence attached.
- Explicit APPROVE or BLOCK.

Clean-audit auto-approval rule:
- When the latest QA site audit is clean (`0` missing assets, `0` permission violations, `0` other failures, `0` config drift), Gate 2 APPROVE must be materialized automatically for the active release.
- Primary path: `scripts/site-audit-run.sh` calls `scripts/gate2-clean-audit-backstop.py` immediately after writing `findings-summary.json`.
- CEO backstop: the scheduled 2-hour CEO cycle (`scripts/ceo-ops-once.sh`, installed by `scripts/install-crons.sh`) re-runs the same remediation and queues a CEO root-cause review item if the backstop had to intervene.
- Purpose: a clean audit is sufficient Gate 2 evidence; duplicate or stale suite-activate churn must not keep PM signoff blocked.

Failing-audit release verdict dispatch rule:
- When an active-release audit is **not** clean, `scripts/site-audit-run.sh` must queue a release-scoped QA inbox item for the owning QA seat in addition to any dev findings items.
- That QA item exists solely to produce one canonical release verdict artifact with the exact release ID and explicit `APPROVE` or `BLOCK`.
- Feature-level QA outboxes, targeted retest notes, and PM prose do **not** satisfy release Gate 2 unless the release-scoped verdict artifact exists in `sessions/qa-<team>/outbox/`.
- If the latest clean audit is later achieved, the clean-audit backstop may still materialize the canonical APPROVE automatically.

Repo-state truth rule for handoffs:
- Any outbox claim of the form `Created: <path>` only counts when that path exists in repo state after execution.
- Executor and supervisor reviews must treat non-existent claimed paths the same way as missing signoff artifacts: the work is **not done** until the file or folder is actually present.

### Release-critical QA testgen backlog intervention rule (PM-owned, added 2026-03-22)

**Trigger (hard threshold):** If a QA testgen backlog for a release-bound grooming pool reaches **2 consecutive groom/improvement cycles with 0 test plans delivered**, PM must intervene directly in the same cycle.

**Intervention decision owner:** PM.

**Default PM intervention (in priority order):**
1. **Resequence the executor**: set all release-bound testgen items to the highest ROI in the queue (`roi.txt` = 50) so they are processed before any other qa seat work.
2. **Cap testgen batch size**: if >8 testgen items are pending for a single release, split into sequential batches of 4 and ensure the first batch fully completes (outbox written, test plans committed) before the next batch starts.
3. **Block Stage-0 scope selection**: PM may NOT run `pm-scope-activate.sh` for any feature without `03-test-plan.md` present. Stage-0 activation is hard-blocked — no negotiation (already required by process flow, but must be explicitly enforced at escalation).
4. **Escalate to Board** only if intervention triggers 3+ consecutive times for the same site in a single release cycle (indicates a structural resourcing problem, not a sequencing problem).

`pm-scope-activate.sh` now seeds flow-managed `agentic_sdlc` handoffs for the activated feature (`Generate Code` for Dev and `Test Cases Review` for QA). From that point on, scope ambiguities and QA failure loops should stay inside LangGraph via exact `Flow outcome:` lines instead of spawning legacy ad hoc `needs-*` artifacts.

**PM responsibility (required):**
- At every groom cycle where testgen items are pending: record the count of pending/completed in the outbox.
- If the threshold above is reached, PM acts immediately on steps 1–3 above and documents the intervention in the outbox.

**Evidence from dungeoncrawler release-b (2026-03-22):**
- 12 testgen items pending since 2026-03-20, 0 delivered, 3 consecutive groom cycles (pm-dungeoncrawler outboxes 20260322-groom-*).
- Stage-0 scope selection for release-b was blocked on missing test plans.
- Root cause: testgen items queued at ROI=43 were not processed before improvement-round items at higher ROI values from other cycles.
- Fix: ROI resequence + batch cap rule (see above).


Required artifacts:
- Release Notes

### Release auto-close policy (scope cap and age — added 2026-04-05)

**Scope cap is a maximum, not a target.** PM MUST NOT hold a release open waiting to fill remaining scope slots.

**Auto-close triggers (either condition closes the release immediately):**
- **Feature count:** ≥ 10 features in_progress for this site
- **Age:** ≥ 24 hours have elapsed since the release was started (i.e. since `release-cycle-start.sh` wrote `tmp/release-cycle-active/<team>.started_at`)

**When either trigger fires, the orchestrator dispatches a `release-close-now` item (ROI 999) to the PM.** PM must act on it in the same inbox cycle:
1. Confirm all in-scope features have Gate 2 APPROVE evidence
2. Defer (Status: ready) any feature that does NOT have Gate 2 APPROVE — it moves to the next release
3. Write Release Notes and record signoff: `./scripts/release-signoff.sh <team> <release-id>`
4. Notify the partner PM for coordinated releases

**PM must never wait for the scope cap to fill.** If QA has approved all in-scope features and either trigger has fired, ship immediately.

### Empty-release Gate 2 waiver procedure (added 2026-04-05 — GAP-IR-20260405-3)

An **empty release** is a release where the auto-close trigger fires but zero features have been activated (`Status: in_progress` with the current `release_id`). This can happen when the orchestrator fires FEATURE_CAP using a cross-release feature count immediately after a new release is created.

**PM responsibility:** if `release-close-now` arrives and 0 features have Gate 2 APPROVE evidence, PM must escalate to CEO immediately (same inbox cycle) with `Status: blocked`, stating "zero features shipped — Gate 2 waiver required."

**CEO waiver procedure:**
1. Create artifact: `sessions/qa-<team>/outbox/YYYYMMDD-gate2-waiver-<release-id>.md`
2. Required content format:
   ```
   # Gate 2 Waiver — <release-id>

   <release-id> — APPROVE — empty release, Gate 2 waived per CEO authority

   ## Waiver rationale
   - <reason release is empty>
   - All scoped features deferred to ready state; zero code changes shipped.
   - No QA evidence can exist for a release with no shipped work.
   - CEO authorizes this waiver to unblock the pipeline.
   - Issued by: ceo-copilot-2
   - Date: YYYY-MM-DD
   ```
3. PM may immediately run `./scripts/release-signoff.sh <team> <release-id>` after the waiver artifact is present.

**Authorization:** Only CEO may issue Gate 2 waivers. PMs may not self-authorize.

Exit criteria:
- Release coordinator confirms coordinated-window readiness (when applicable).
- Tester approves.
- Dev confirms deploy steps/rollback and that all changes are committed (commit hash(es) recorded).
- **Schema deploy gate (required when schema changes exist):** Dev must run `drush --uri=<site-uri> updatedb --status` on each production target and execute any pending updates. Output must appear in release notes or implementation notes. If no schema changes: explicitly state "no schema changes in this release." (Added 2026-04-05 — GAP-DC-SCHEMA-DEPLOY: two CRITICAL production bugs caused by missing `drush updatedb` post-deploy in dungeoncrawler release-next. Fix was applied in dev-dungeoncrawler seat instructions but was absent from the shared gate, leaving all other dev seats exposed to the same failure class.)

Coordinated release rule (Forseti + Dungeoncrawler):
- All required coordinated PM seats must sign off before the official push:
	- `./scripts/release-signoff.sh <site-or-team-alias> <release-id>`
- Required seats are resolved from `org-chart/products/product-teams.json` where `active=true` and `coordinated_release_default=true`.
- Release operator (`pm-forseti`) verifies:
	- `./scripts/release-signoff-status.sh <release-id>`
- Per-team release ID registration (required): each coordinated PM seat must also record a per-team signoff for their own release ID in addition to the shared coordinated ID:
	- `./scripts/release-signoff.sh dungeoncrawler <per-team-release-id>`
	- This ensures improvement-round.sh detects the release at the correct time and avoids retroactive signoff artifacts being created later by workspace merges.
- Cross-team PM signoff check (required): each coordinated PM seat must verify the OTHER team's release ID also has a signoff before the release operator pushes. Example: pm-forseti must confirm pm-dungeoncrawler signed `<dungeoncrawler-release-id>`, and vice versa. Verify with `./scripts/release-signoff-status.sh <partner-release-id>`. If missing, the push is blocked until the partner PM signs. (Added 2026-03-27 — GAP-FST-27-04: pm-forseti missed dungeoncrawler signoff in `20260326-dungeoncrawler-release-b` coordinated push.)

### Push boundary handoff (between readiness and post-release verification)

The official push is triggered by a **queue artifact**, not by a free-form PM decision:

1. `scripts/release-signoff.sh <team> <release-id>` writes the PM signoff artifact.
   - If the artifact file is absent after a claimed signoff, treat the release as unsigned regardless of any PM outbox prose.
2. When all required coordinated PM signoffs exist, the same script creates:
   - `sessions/<operator-pm>/inbox/<ts>-push-ready-<release>/command.md`
3. The release operator consumes that inbox item and performs the official push.
4. Immediately after a successful push, the operator runs:
   - `bash scripts/post-coordinated-push.sh [team-id ...]`

Only after step 4 may runtime release pointers advance and post-release QA artifacts begin.

## Gate 4 — Post-release verification (Tester, production)
Required artifacts:
- Post-release verification note (may reuse Verification Report format)

Exit criteria:
- Tester runs the same audit protocol against production base URL(s).
- If clean: Tester explicitly reports “post-release QA clean” and “no new items identified for Dev”.
- If unclean: Tester records the unclean signal with evidence.

Policy:
- If post-release is unclean, the next release cycle is remediation-only (no new features).
- PM escalates to Board if there are 3 unclean releases in a row for a product/site.

## Coordinated Release
Additional rules for shipping:
- Forseti and Dungeoncrawler pushes happen in the same release window.
- Release operator (`pm-forseti`) owns the go/no-go decision for coordinated releases.

Runbook: `runbooks/coordinated-release.md`
