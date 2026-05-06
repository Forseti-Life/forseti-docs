# Lesson: Release Gate Re-Queue Loop (2026-05-06)

## Issue
A release gate task re-queueing loop created 657 duplicate code review gate tasks for two releases (`20260412-dungeoncrawler-release-u` and `20260412-forseti-release-r`) in approximately 2 hours on 2026-05-05.

**Symptoms:**
- CEO inbox flooded with nearly identical gate tasks (584 + 73 items)
- Gate tasks created every ~12 seconds
- Release workflow blocked despite gate marker files indicating releases were pushed
- Exponential task accumulation with no deduplication

## Root Cause
**LangGraph orchestration design flaw:** The `coordinated_push` node runs on every tick (~12 second interval) without interval gating, while `release_cycle` node has proper interval gating (5 minutes).

Flow:
1. `release_cycle` node checks interval; only runs every 5 minutes when interval elapses
2. `coordinated_push` node runs **unconditionally** on every tick
3. `coordinated_push` calls `run_coordinated_push_step()` → `check_code_review_gate()`
4. Gate deduplication check (`gate_already_queued`) uses `any()` over inbox directory
5. On first ~5 minutes, gate check encounters no existing gates (before first gate creation)
6. After first gate is created, deduplication should prevent new gates
7. **However**, gate creation happened every ~12 seconds, not every 5 minutes

**Why deduplication didn't work initially:**
The `gate_already_queued` check DOES work correctly. The issue was that `check_code_review_gate` was being called 25x per 5-minute window, whereas it should have been called once.

## Solution
**Add interval gating to `run_coordinated_push_step()`** (60-second interval).

File: `orchestrator/release_cycle.py`
- Added timestamp tracking in `tmp/coordinated-push-last-run.ts`
- Function skips execution if called within 60 seconds of last run
- Reduces gate task creation checks from ~300x/hour to ~1x/minute

## Prevention
- **Pattern:** Always add interval gating to recurring orchestration steps that perform I/O or state checks
- **Code review:** LangGraph nodes without interval gating should be flagged
- **Monitoring:** Track inbox growth rate; exponential growth indicates re-queueing loops
- **Automation:** Implement inbox saturation alerts (>500 items of same type = potential loop)

## Commit
- Fix: `8712289752` (orchestrator/release_cycle.py: +27 lines)

## Cleanup
- Archived 657 old gate tasks to `sessions/ceo-copilot-2/inbox/_archived/`
- Verified no new gates created on 2026-05-06 (interval gate working)

## References
- DECISION_OWNERSHIP_MATRIX: Issue type "Process/rule ambiguity"
- Troubleshooting protocol: Applied "trace live logic" → "identify current state" → "fix it"
