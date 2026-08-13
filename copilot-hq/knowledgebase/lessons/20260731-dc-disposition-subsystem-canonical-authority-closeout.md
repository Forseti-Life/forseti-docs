# Lesson Learned: Dungeoncrawler disposition subsystem canonical-authority closeout

- Date: 2026-07-31
- Agent(s): ceo-copilot-2
- Website: dungeoncrawler.app
- Module(s): dungeoncrawler-content

## What happened

A large multi-phase architecture inbox item implemented canonical authority convergence for disposition, aggression, combat-entry, stance runtime, and shared actor-context projections. The risk after implementation was organizational drift: future teams could re-open solved seams or reintroduce legacy fallbacks if completion evidence was not registered outside the inbox thread.

## Root cause

Historically, completion state has lived mostly inside per-item inbox artifacts. Without explicit registration in knowledgebase + scoreboards + outbox closeout, cross-team memory can decay and later work can treat completed architecture as still-open.

## Impact

If not registered, future planning could duplicate work, re-add legacy `som_state`/heuristic reads, or mis-prioritize stale architecture remediation as active debt. That would inflate cycle time and increase regression risk.

## Detection / Signals

- Gate scorecard reached full completion across phases 1-11.
- Contract sweep for all touched seams passed.
- Inbox README still had stale “still open” language until closeout normalization.

## Fix applied (if any)

- Closed the inbox item with full gate scorecard completion evidence.
- Archived the item from active inbox to `_archived`.
- Added this org-level lesson to register the subsystem as completed canonical authority work.
- Updated item docs to retain only a post-gate validation backlog (live smoke + legacy-save sanity pass).

## Prevention (process + code)
- For any architecture item spanning multiple phases, require:
  1. gate-based completion table,
  2. full touched-contract validation sweep,
  3. outbox closeout entry,
  4. knowledgebase lesson registration before archive.
- Treat canonical disposition/aggression/stance/combat-entry services as the only forward mutation/read authority in new work.

## References
- sessions/ceo-copilot-2/inbox/_archived/20260730-attitude-stance-combat-architecture/README.md
- sessions/ceo-copilot-2/inbox/_archived/20260730-attitude-stance-combat-architecture/IMPLEMENTATION_PHASE_PLAN.md
- sessions/ceo-copilot-2/outbox/20260731-attitude-stance-combat-architecture-closeout.md
