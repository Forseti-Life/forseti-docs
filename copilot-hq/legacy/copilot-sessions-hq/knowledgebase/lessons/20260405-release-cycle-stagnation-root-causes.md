# Lesson: Release Cycle Stagnation — Root Causes and Remediation (2026-04-05)

**Discovered by:** CEO (Forseti) post-mortem on 11-day stagnation 2026-03-22 → 2026-04-02

---

## What happened

The org stagnated for 11 days. Orchestrator was running the entire time (600+ ticks/day),
but no release work was being done and no agents were advancing the release cycle.

## Root causes confirmed (with evidence)

### 1. Signoff file was never written (primary cause)
The orchestrator advances the release cycle when:
`sessions/pm-<team>/artifacts/release-signoffs/<current-release-id>.md` exists.

The signoff file for `20260322-dungeoncrawler-release` was not written until 2026-04-02
(confirmed by `stat` mtime). Without it, `_release_cycle_step` held in place indefinitely.

**Why**: No dev work was dispatched for the current release (see cause 3), so PM had nothing to sign off on.

### 2. Stale blocked agents consumed all exec capacity
Four agents (agent-explore-infra, ba-forseti, ba-dungeoncrawler, dev-dungeoncrawler) had
`needs-info` inbox items dating from February that were never archived. Every orchestrator
tick selected one of these 4 agents as the non-CEO exec slot. Real release work never ran.

The orchestrator had no auto-archive policy for stale `needs-info` items.

**Fix**: `_auto_archive_stale_blocked()` now runs in `_health_check_step` — items with
`needs-info` outbox older than 5 days are auto-archived.

### 3. No scope activation dispatched on cycle start (structural gap)
`release-cycle-start.sh` dispatches QA preflight + PM groom for NEXT release only.
Nothing triggers `pm-scope-activate.sh` for the CURRENT release's features.
With no dev impl items dispatched, dev-<team> had nothing to implement.

**Fix**: `release-cycle-start.sh` now dispatches a `needs-ceo-copilot-scope-activate`
CEO inbox item (ROI=20) on every cycle start. CEO must promptly run
`pm-scope-activate.sh <team> <feature>` for each groomed feature.

### 4. `gh` CLI not installed → LangGraph tick crash
On 2026-03-22, when `release-push.sh` returned rc≠0, the fallback called
`gh workflow run` — but `gh` was not installed. Python `subprocess.run` raised
`FileNotFoundError`, which LangGraph re-raised, aborting the entire tick.

**Fix**: `gh` CLI installed (v2.45.0). `_coordinated_push_step` now wraps the `gh`
call in `try/except FileNotFoundError` and logs a warning instead of crashing.

### 5. Path migration not completed (ba-forseti write block)
The repo moved from `/home/keithaumiller/` to `/home/ubuntu/` but agent instructions,
exec prompts, and site configs still referenced the old path. The `agent-exec-next.sh`
prompt told every agent its repos were at `/home/keithaumiller/` — meaning agents trying
to write files were targeting nonexistent paths, which the tool sandbox rejected as
`"Permission denied and could not request permission from user"`.

**Fix**: Mass sed replacement across 1200+ files. All paths now reference `/home/ubuntu/`.

### 6. Improvement-round flood after cycle advance
When the cycle finally advanced on 2026-04-02, `improvement-round.sh` dispatched items
to ALL seats. These outranked active release work (improvement-round ROI=3 is already
below QA preflight ROI=9, but the items that were dispatched had varying ROIs). The
queue cleared only after manual archival of ~30 items.

---

## Detection pattern (how to spot this recurring)

```
tick: agents=ceo-copilot-2,<same 4 agents>,...
```
If the orchestrator log shows the **same 4 agents on every tick for > 1 day**:
blocked agents are consuming exec capacity. Check `hq-blockers.sh`.

If `sla-report.sh` shows `outbox-lag` for ALL active seats with age > 1800s:
nothing is being worked. Trace back to release cycle state.

---

## Remediation steps (in order)

1. `bash scripts/sla-report.sh` — identify breach types
2. `bash scripts/hq-blockers.sh` — archive any stale needs-info items
3. `cat tmp/release-cycle-active/*.release_id` — identify current release IDs
4. Check signoffs: `ls sessions/pm-*/artifacts/release-signoffs/` — does the current release file exist?
5. If no signoff: check dev impl items. If none, run `pm-scope-activate.sh <team> <feature>` for each groomed feature.
6. Check improvement-round flood: archive items predating current release start
7. Run `sla-report.sh` again — should show only valid active items

---

## References
- CEO outbox: `sessions/ceo-copilot/outbox/20260405-stagnation-full-analysis.md`
- Commits: `b88ed153`, `e4cb56b5`, `89d6bab6`, `6ac79c6e`
