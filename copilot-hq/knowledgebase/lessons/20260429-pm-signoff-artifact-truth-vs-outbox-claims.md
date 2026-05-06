# Lesson: PM signoff truth comes from the artifact, not the outbox

- Date: 2026-04-29
- Team: forseti + dungeoncrawler
- Releases: `20260412-forseti-release-v`, `20260412-dungeoncrawler-release-y`
- Blocker class removed: `False PM-signoff completion caused by success-shaped outboxes without signoff artifacts`

## What happened

Both PM seats produced outbox text claiming they had executed `scripts/release-signoff.sh`, but the actual signoff artifacts were missing and `scripts/release-signoff-status.sh` still reported both releases as unsigned.

This created a false system narrative:
- PM outboxes said signoff was complete
- CEO/session summaries repeated that assumption
- release health still blocked because it correctly checked the artifact path

In parallel, dungeoncrawler release-y was not actually ready for truthful signoff yet because the release code review still reported unresolved MEDIUM+/HIGH findings without routing or risk-acceptance evidence.

## Root cause

1. PM outbox completion was not tied tightly enough to repo-state proof.
2. Supervisory follow-up treated outbox prose as equivalent to signoff artifacts.
3. Signoff reminder/readiness flow did not verify Gate 1b closure before asking PM to sign.

## Fix applied

- Updated `runbooks/shipping-gates.md` to make the signoff artifact the explicit source of truth and to require MEDIUM+ code-review routing/risk acceptance before signoff reminders/readiness claims.
- Updated `org-chart/agents/instructions/pm-forseti.instructions.md` so PM signoff work cannot be marked `done` until:
  - `sessions/pm-forseti/artifacts/release-signoffs/<release-id>.md` exists, and
  - `bash scripts/release-signoff-status.sh <release-id>` reflects the new state

## Prevention going forward

- Do not treat a PM outbox sentence like "ran release-signoff.sh" as completion.
- Check the artifact file first; if it does not exist, signoff did not happen.
- For releases with code-review findings, verify every MEDIUM+ item is routed to Dev or risk-accepted before dispatching PM signoff work.
- If a PM cannot run commands in-context, they must leave the item `in_progress` or `blocked`, not `done`.
