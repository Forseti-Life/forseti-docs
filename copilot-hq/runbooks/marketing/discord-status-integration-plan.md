# Discord Status Integration — Implementation Plan

## Goal

Deliver a production-safe Discord status publisher for marketing updates covering `forseti.life` and `dungeoncrawler`.

## Phase 1 — Documentation baseline (current)

Deliverables:
- Architecture definition
- Process-flow definition
- Implementation plan

Exit criteria:
- Scope and constraints are explicit
- Channel boundary (Discord only) is documented

## Phase 2 — Tool implementation

Deliverables:
- `scripts/marketing/discord_feature_updates.py`

Required behavior:
- Configurable lookback window and max entries
- Discovers local repos under `/home/ubuntu/forseti.life` (configurable)
- Queries local git commits within lookback window
- Queries GitHub commits for discovered repository origins within lookback window
- Deduplicates and classifies commit subjects into feature enhancements and improvements/fixes
- Renders bounded Discord-safe message
- Supports `--dry-run` and optional `--skip-empty`
- Fails hard on bad config/query/delivery errors

Exit criteria:
- Manual dry run produces expected message
- Live post path returns success with valid webhook

## Phase 3 — Scheduler integration

Deliverables:
- `scripts/install-cron-marketing-discord-updates.sh`

Required behavior:
- Idempotent cron install/update with marker
- Logs to `inbox/responses/marketing-discord-feature-updates-cron.log`
- Uses file/env webhook config (no hardcoded secret)
- Uses file/env GitHub token config (no hardcoded secret)

Exit criteria:
- Installer writes one canonical cron line
- Re-running installer does not duplicate entries

Install command:
```bash
cd /home/ubuntu/forseti.life/copilot-hq
DISCORD_WEBHOOK_FILE=/absolute/path/to/discord-webhook.txt \
bash scripts/install-cron-marketing-discord-updates.sh
```

## Phase 4 — Validation and rollout

Validation checklist:
- Script syntax check passes
- Dry-run output format is readable and bounded
- Cron command path executes successfully when run manually
- Discord delivery verified in target channel

Manual dry-run command:
```bash
cd /home/ubuntu/forseti.life/copilot-hq
scripts/marketing/run-discord-feature-updates.sh --dry-run
```

Rollout:
1. Install cron.
2. Run one forced/manual post to verify.
3. Monitor first scheduled runs for delivery stability.

## Phase 5 — Handoff to marketing seat

Deliverables:
- Usage notes in seat artifacts/instructions as needed
- Confirmation that `marketing-forseti` owns this tool path

Exit criteria:
- Tool ownership and operating responsibility are explicit and accepted
