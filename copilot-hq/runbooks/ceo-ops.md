# Forseti CEO ops cadence

This runbook is the **quick technical reference** for the automated CEO monitoring
loop: what cron fires, what script it invokes, how that turns into a CEO cycle,
and which helper scripts execute in what order.

## Quick answer

The installed cron entry is:

```cron
*/10 * * * * python3 /home/ubuntu/forseti.life/scripts/ceo-ops-scheduler.py >> /home/ubuntu/forseti.life/inbox/responses/ceo-ops-cron.log 2>&1
```

That means cron invokes the **CEO scheduler every 10 minutes**. The scheduler does
not always run a full CEO cycle. It decides whether to run `scripts/ceo-ops-once.sh`
now or just log a skipped relaxed-cycle check.

## Execution chain

```text
cron every 10m
→ scripts/ceo-ops-scheduler.py
  → read tmp/ceo-ops-scheduler-state.json
  → if cadence allows: bash scripts/ceo-ops-once.sh
  → parse FAIL lines from output
  → update scheduler state
  → if the same blocker persists, queue a CEO RCA inbox item
```

## Scheduler behavior

State file:

- `tmp/ceo-ops-scheduler-state.json`

Decision logic:

1. If `fast_mode` is `true`, run the full CEO cycle on every 10-minute cron tick.
2. Otherwise, only run when both are true:
   - `now.minute == 0`
   - `now.hour % RELAXED_INTERVAL_HOURS == 0`
3. Default relaxed interval:
   - `RELAXED_INTERVAL_HOURS = 2`

Effects:

- **Healthy/quiet system** → full CEO loop runs on the 2-hour boundary.
- **Failing system** → scheduler flips to `fast_mode`, so the full CEO loop runs
  every 10 minutes until health clears.

Skip logs:

- `inbox/responses/ceo-ops-latest.log`
- `inbox/responses/ceo-ops-YYYYMMDD.log`

Main cron log:

- `inbox/responses/ceo-ops-cron.log`

## `scripts/ceo-ops-once.sh` call order

When the scheduler decides to run a full CEO cycle, `scripts/ceo-ops-once.sh`
executes in this order:

1. Read and print priority rankings from `org-chart/priorities.yaml`
2. Run `./scripts/hq-status.sh`
3. List CEO inbox items from `sessions/ceo-copilot-2/inbox/`
4. Run Gate 2 clean-audit backstop:
   - `python3 ./scripts/gate2-clean-audit-backstop.py --source "ceo-ops-once.sh" --queue-followup`
5. Run pipeline remediation dispatch:
   - `python3 ./scripts/ceo-pipeline-remediate.py --source "ceo-ops-once.sh"`
6. Run project registry link audit:
   - `python3 ./scripts/project-registry-link-audit.py`
7. Run release health:
   - `./scripts/ceo-release-health.sh`
8. Run system health with dispatch enabled:
   - `./scripts/ceo-system-health.sh --dispatch`
9. Print blockers snapshot:
   - `./scripts/hq-blockers.sh | head -n 200`
10. Emit suggested CEO actions based on the above return codes and blocker counts

If major checks fail, `ceo-ops-once.sh` exits nonzero. The scheduler uses that to
turn on `fast_mode`.

## What the two CEO health scripts cover

### `scripts/ceo-release-health.sh`

Release-pipeline diagnostic for active coordinated teams:

- runtime `release_id` / `next_release_id`
- Gate 2 evidence
- PM signoffs
- cross-team signoffs
- coordinated push readiness
- deploy workflow status
- orphaned/stale release features
- backlog health

### `scripts/ceo-system-health.sh --dispatch`

Systemic ops diagnostic plus inbox dispatch generation:

- executor failures
- orchestrator health
- automation duplication / Copilot pressure
- merge health
- Apache error logs
- Drupal watchdog
- scoreboard freshness
- feature velocity
- KB lesson rate
- Drupal queue health
- QA audit freshness
- dead-letter inbox detection

With `--dispatch`, this script creates inbox items for the owning seats when it
finds actionable failures.

### `scripts/ceo-repo-health.sh`

On-demand repo creep / duplication scan for deeper filesystem-wide git analysis:

- inventories git repos from a scan root
- maps local paths to primary GitHub upstream repos
- highlights duplicate local copies of the same upstream repo
- flags likely side-workspaces / repo creep outside ownership metadata

This script is **not** part of the default CEO scheduler loop. Use it when a deeper
repo-hygiene investigation is needed.

## Related loops

This CEO ops cadence is only one part of the overall system:

- **Manual CEO session** — driven by the CEO seat instructions
- **Scheduled CEO monitoring** — this runbook
- **Continuous orchestrator loop** — `scripts/orchestrator-loop.sh` → `orchestrator/run.py`

For the interactive CEO execution order, see:

- `org-chart/agents/instructions/ceo-copilot-2.instructions.md`
