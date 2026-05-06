# Lesson: Release Gate 1b code review was not actually in LangGraph

- Date: 2026-04-29
- Team: forseti + dungeoncrawler
- Blocker class removed: `Release code-review findings existed but did not progress because they were outside flow routing`

## What happened

We had pending release code-review artifacts with MEDIUM+/HIGH findings that were not being routed to Dev or converted into PM risk-acceptance artifacts. At first glance this looked like a stuck LangGraph flow.

The real state was different:
- `agentic_sdlc` does have a `Code Review` node
- but release-cycle pre-ship review is **not** that node
- release-cycle automation writes a plain `agent-code-review` inbox item with no `Flow id` metadata
- the flow router therefore never advances those review results into PM/Dev follow-up

This left Gate 1b depending on manual PM behavior while later automation still created signoff prompts.

## Root cause

1. Release Gate 1b review used a legacy artifact-only path outside `agentic_sdlc`.
2. PM follow-up for MEDIUM+ findings was documented but not enforced in automation.
3. Signoff automation checked for missing PM signoff artifacts without checking whether release-review findings were still unresolved.

## Fix applied

- Added a reusable code-review gate checker:
  - `scripts/lib/code_review_gate.py`
  - `scripts/check-code-review-routing.py`
- `scripts/release-signoff.sh` now blocks signoff if release-review findings remain unrouted.
- `orchestrator/dispatch.py` now queues `code-review-followup` instead of `awaiting-signoff` when Gate 1b is still open.
- `scripts/ceo-pipeline-remediate.py` now queues `code-review-followup` instead of `signoff-reminder` when unresolved release-review findings are present.

## Prevention going forward

- Do not assume every review artifact belongs to LangGraph just because `agentic_sdlc` has a `Code Review` node.
- Treat release Gate 1b as a separate gate until/unless it is explicitly modeled as a flow-managed node.
- Never prompt PM signoff until the release-review findings are either:
  - routed to Dev as `cr-finding` work, or
  - captured in PM risk-acceptance artifacts.
