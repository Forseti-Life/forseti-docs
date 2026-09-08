# KB Lesson: Harness Context Limit Must Be Fixed, Not Bypassed

## Date
2026-09-08

## Symptom
`scripts/agent-exec-next.sh ba-dungeoncrawler` failed with
`local llama-server HTTP 400: request (9785 tokens) exceeds the available
context size (8192 tokens)`. The architect seat silently picked a different
(smaller) inbox item instead of the intended review.

## Root Cause
The harness inlines the full instruction stack plus `command.md` into one
prompt; the host-local Qwen2.5-3B server runs with `--ctx-size 8192`. A
CEO-authored spec-review item exceeded that budget. There is no preflight
size check, so the failure surfaces only as an HTTP 400 from the model.

## What Went Wrong Operationally
The CEO thread ran the architect, BA and PM seats as ad-hoc Copilot CLI
sub-agents outside the harness so the work would progress. Output quality
was fine, but this bypassed the HQ automation framework: no harness session,
no ROI selection, no rate/concurrency guards, no orchestrator visibility.
The Board flagged it. Outputs produced that way are marked in the relevant
`status.md` files as `runtime: ceo-invoked copilot-cli (outside harness)`.

## Rule
When the framework cannot execute an item, the CEO fixes the framework
(dispatch an infra item, or re-size the work item) — never runs the seat's
work by another route. Board approval is required for any exception.

## Permanent Fix
`sessions/dev-infra/inbox/20260908-hq-harness-context-limit`: raise
`CTX_SIZE` (Qwen2.5-3B supports 32k), add `prompt_exceeds_context` preflight
in `agent-exec-next.sh`, assert `n_ctx` in `verify-hq-runtime.sh`, and add
the "command.md must fit the harness budget; reference packets by path" rule
to `org-wide.instructions.md`.
