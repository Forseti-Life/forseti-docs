# Repo health monitor

## Purpose

`scripts/ceo-repo-health.sh` is an **on-demand** repo inventory and creep/duplication detector for CEO/system-health use.

It is **not** part of the default 10-minute CEO monitoring loop. Use it when you want a deeper filesystem-wide git-repo scan.

## What it checks

- all git repositories reachable from the scan root
- primary remotes and GitHub upstream repo mappings
- duplicate local copies of the same upstream repo
- likely repo creep / side workspaces, including:
  - `/tmp/*`
  - `/root/.copilot/session-state/*`
  - `/home/ubuntu/repo-work/*`
  - unowned repos not present in `org-chart/ownership/repository-ownership.yaml`

## Usage

```bash
cd /home/ubuntu/forseti.life

# report to stdout, exit 1 if duplicates/creep are found
bash scripts/ceo-repo-health.sh

# write markdown + TSV artifacts
bash scripts/ceo-repo-health.sh --report-dir /tmp/dungeoncrawler-rca

# JSON summary for tooling
bash scripts/ceo-repo-health.sh --json
```

## Output artifacts

When `--report-dir <dir>` is used, the script writes:

- `<dir>/repo-health-report.md`
- `<dir>/repo-health-scan.tsv`

## Current intended usage

Run this after cleanup/migration work or before deeper CEO RCA when you want to detect:

1. duplicate local clones/worktrees of the same GitHub repo
2. temporary workspaces that accumulated outside canonical repo roots
3. repos on disk that are not represented in repository ownership metadata
