<!-- REVIEWED: 2026-07-16 -->
# Copilot HQ Documentation

This directory is the canonical documentation home for
[`Forseti-Life/copilot-hq`](https://github.com/Forseti-Life/copilot-hq).

## Contents

- `runbooks/` - operational procedures and repeatable workflows
- `knowledgebase/` - lessons learned, reviews, scoreboards, and proposals
- `org-chart/ownership/` - repository, module, and file ownership references
- `legacy/copilot-sessions-hq/` - archived legacy-only artifacts preserved during retirement of the old `keithaumiller/copilot-sessions-hq` checkout

`copilot-hq` keeps compatibility links at `runbooks/`, `knowledgebase/`, and
`org-chart/ownership/` so the runtime and existing paths continue to work from
the HQ checkout while this repo remains the source of truth.

The managed repository workspace root is `/home/ubuntu/forseti.life`. The
canonical HQ repo root is `/home/ubuntu/forseti.life/copilot-hq`, while product
and module development should happen in the owning sibling repositories under
`/home/ubuntu/forseti.life/*`.

## Agentic Development Readiness

- **Quick start:** Read `copilot-hq/README.md` and capture the current scope before editing. Cross-check `README.md` to align terms, boundaries, and linked issue context. Validate repository-level consistency against `README.md` before publishing.
- **Key entry points:** `README.md`, `ARCHITECTURE.md`, `copilot-hq/knowledgebase/README.md`, `copilot-hq/knowledgebase/lessons/README.md`
- **Verification:** Run `git --no-pager grep -n "## Agentic Development Readiness" "copilot-hq/README.md"`; then run `git --no-pager grep -n "^#" "README.md"`.
- **Source of truth:** the HQ checkout while this repo remains the source of truth.
- **Constraints / gotchas:** All agents MUST read the target repository instructions before making changes.
- **Architecture map:** `copilot-hq/README.md`, `README.md`, `ARCHITECTURE.md`, `copilot-hq/knowledgebase/README.md`, `copilot-hq/knowledgebase/lessons/README.md`
