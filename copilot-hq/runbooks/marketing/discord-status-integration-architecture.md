# Discord Status Integration — Architecture

## Scope

This architecture defines the initial marketing automation for posting status updates to Discord for:
- `forseti.life`
- `dungeoncrawler`

Initial channel scope is intentionally limited to Discord only.

## Objective

Provide a deterministic, cron-safe tool that queries GitHub and local forseti repositories, then publishes a concise summary of improvements and feature enhancements from the last few days.

## System boundaries

### In scope
- Read recent commit activity from local git repositories under `/home/ubuntu/forseti.life`.
- Query GitHub commit APIs for discovered repository origins.
- Merge/dedupe local and GitHub commit views for one authoritative summary set.
- Format a bounded Discord message.
- Deliver via Discord webhook.
- Run from cron.

### Out of scope (initial phase)
- Posting to email/social/blog channels.
- Auto-reply loops or bi-directional Discord command handling.
- Marketing campaign generation beyond status summaries.

## Components

1. **Scheduler**
   - Cron entry invokes the Discord status publisher at a fixed cadence.

2. **Commit source collector**
   - Local git log collection across discovered repos in the configured root.
   - GitHub API commit collection per discovered `owner/repo` origin.
   - Lookback window constrained by configurable `N` days.

3. **Commit classifier**
   - Classifies commit subjects into:
     - feature enhancements
     - improvements/fixes

4. **Message renderer**
   - Builds one canonical post body.
   - Enforces max-item and max-length bounds for Discord.

5. **Discord delivery client**
   - Sends `POST` payload to webhook endpoint.
   - Treats non-2xx/204 responses as hard failures.

## Artifact map

- Publisher: `scripts/marketing/discord_feature_updates.py`
- Cron installer: `scripts/install-cron-marketing-discord-updates.sh`
- Runtime log target: `inbox/responses/marketing-discord-feature-updates-cron.log`

## Configuration contract

- `MARKETING_FEATURE_UPDATE_DAYS` (default: `3`)
- `MARKETING_FEATURE_UPDATE_MAX_ITEMS` (default: `10`)
- `MARKETING_REPO_ROOT` (default: `/home/ubuntu/forseti.life`)
- `DISCORD_WEBHOOK_URL` **or** `DISCORD_WEBHOOK_FILE`
- `GITHUB_TOKEN` **or** `GITHUB_TOKEN_FILE` (default file: `/home/ubuntu/github.token`)

Secrets are environment/file sourced only; never stored in repository content.

## Failure and reliability model

- Hard-fail on:
  - missing/invalid webhook configuration
  - local git query failure
  - GitHub query/auth failure
  - Discord HTTP delivery failure
- If no developer updates are present in the lookback window, exit `0` with no generated/post attempt.

## Security model

- Webhook is treated as sensitive credential.
- GitHub token is treated as sensitive credential.
- No secret values echoed into logs.
- Logs contain operational status only (counts, window, repos, success/failure).

## Ownership

- Seat owner: `marketing-forseti`
- Supervisor: `ceo-copilot-2`
- Implementation surface: `scripts/marketing/**` and cron installer under `scripts/`.

## Standard outbound message format

The default/standard Discord post format is plain-text and concise:
- Header: `Forseti Product Update (last N days)`
- Timestamp line: `Generated: ...`
- `Delivery snapshot` section
- `Top feature/improvement groups (player + developer impact)` section
- Numbered grouped updates with:
  - `Players: ...`
  - `Developers: ...`

Formatting rules for this standard:
- No emoji
- Minimal markdown emphasis
- Keep list noise low (numbered groups, short lines)
